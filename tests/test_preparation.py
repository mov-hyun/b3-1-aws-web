import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_user_data", ROOT / "scripts" / "build_user_data.py")
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class PreparationTests(unittest.TestCase):
    def test_shell_does_not_expand_html(self):
        html = '<p>$(touch /tmp/unexpected) $HOME `id`</p>'
        script = BUILD.build_script(html, "server {}")
        self.assertIn("<<'B31_HTML_END'\n" + html, script)

    def test_rejects_heredoc_termination_in_source(self):
        with self.assertRaises(ValueError):
            BUILD.build_script("B31_HTML_END\ntouch /tmp/unexpected", "server {}")

    def test_rejects_ec2_userdata_over_limit(self):
        with self.assertRaises(ValueError):
            BUILD.build_script("한" * 6000, "server {}")

    def test_policy_security_boundaries(self):
        policy = json.loads((ROOT / "infra" / "iam-policy.json").read_text())
        self.assertLessEqual(len(json.dumps(policy, separators=(",", ":"))), 6144)
        for statement in policy["Statement"]:
            condition = statement["Condition"]
            self.assertEqual(condition["StringEquals"]["aws:RequestedRegion"], "ap-northeast-2")
            self.assertEqual(condition["Bool"]["aws:MultiFactorAuthPresent"], "true")
            actions = statement["Action"]
            for action in [actions] if isinstance(actions, str) else actions:
                self.assertTrue(action.startswith("ec2:"))
                self.assertNotIn(action, ["ec2:*", "ec2:AllocateAddress", "ec2:CreateNatGateway", "ec2:PurchaseReservedInstancesOffering"])
        statements = {s["Sid"]: s for s in policy["Statement"]}
        self.assertEqual(statements["LaunchTaggedMicroWithImdsv2"]["Condition"]["StringEquals"]["ec2:InstanceType"], "t3.micro")
        self.assertEqual(statements["OperateAndCleanOnlyTaggedLabResources"]["Condition"]["StringEquals"]["aws:ResourceTag/Project"], "b3-1")


if __name__ == "__main__":
    unittest.main()
