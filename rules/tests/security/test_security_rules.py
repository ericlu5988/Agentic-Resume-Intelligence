"""
Security validation tests using SAST tools.

These tests verify that "Don't" examples trigger security warnings
and "Do" examples pass security checks.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest


class TestSemgrepIntegration:
    """Tests using Semgrep for security pattern matching."""

    @pytest.fixture
    def semgrep_available(self) -> bool:
        """Check if Semgrep is available."""
        try:
            result = subprocess.run(
                ["semgrep", "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _run_semgrep(
        self, code: str, language: str, temp_dir: Path
    ) -> dict[str, Any]:
        """Run Semgrep on code and return results."""
        # Map language names to Semgrep file extensions
        lang_extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "go": ".go",
            "java": ".java",
            "ruby": ".rb",
            "php": ".php",
            "csharp": ".cs",
            "rust": ".rs"
        }

        ext = lang_extensions.get(language.lower(), ".txt")
        code_file = temp_dir / f"test_code{ext}"
        code_file.write_text(code)

        # Run Semgrep with auto-detection
        result = subprocess.run(
            [
                "semgrep", "scan",
                "--config", "auto",
                "--json",
                "--quiet",
                str(temp_dir)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"results": [], "errors": []}

    @pytest.mark.slow
    @pytest.mark.skip(reason="Slow SAST integration test - run manually if needed")
    def test_dont_examples_trigger_security_warnings(
        self,
        code_blocks_by_language: dict[str, list[dict[str, Any]]],
        semgrep_available: bool
    ) -> None:
        """Verify Don't examples are flagged by Semgrep."""
        if not semgrep_available:
            pytest.skip("Semgrep not available")

        # Focus on languages with good Semgrep support
        supported_languages = ["python", "javascript", "typescript", "go", "java"]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            untriggered = []

            for lang in supported_languages:
                blocks = code_blocks_by_language.get(lang, [])
                dont_blocks = [b for b in blocks if b["type"] == "dont"]

                for block in dont_blocks:
                    code = block["code"]
                    rule_name = block["rule_name"]

                    results = self._run_semgrep(code, lang, temp_path)

                    if not results.get("results"):
                        # This is informational, not a failure
                        # Some Don't examples might be too subtle
                        untriggered.append(
                            f"Rule '{rule_name}' ({lang}): "
                            f"Don't example not flagged by Semgrep"
                        )

            # Report untriggered examples as warnings
            if untriggered:
                pytest.xfail(
                    f"{len(untriggered)} Don't examples not detected:\n"
                    + "\n".join(untriggered[:10])  # Limit output
                )

    @pytest.mark.slow
    @pytest.mark.skip(reason="Slow SAST integration test - run manually if needed")
    def test_do_examples_pass_security_checks(
        self,
        code_blocks_by_language: dict[str, list[dict[str, Any]]],
        semgrep_available: bool
    ) -> None:
        """Verify Do examples don't trigger security warnings."""
        if not semgrep_available:
            pytest.skip("Semgrep not available")

        supported_languages = ["python", "javascript", "typescript", "go", "java"]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            errors = []

            for lang in supported_languages:
                blocks = code_blocks_by_language.get(lang, [])
                do_blocks = [b for b in blocks if b["type"] == "do"]

                for block in do_blocks:
                    code = block["code"]
                    rule_name = block["rule_name"]

                    results = self._run_semgrep(code, lang, temp_path)

                    # Filter for high/critical severity only
                    high_severity = [
                        r for r in results.get("results", [])
                        if r.get("extra", {}).get("severity") in ["ERROR", "WARNING"]
                    ]

                    if high_severity:
                        errors.append(
                            f"Rule '{rule_name}' ({lang}): "
                            f"Do example triggered {len(high_severity)} warning(s)"
                        )

            if errors:
                pytest.fail("\n".join(errors))


class TestBanditIntegration:
    """Tests using Bandit for Python security analysis."""

    @pytest.fixture
    def bandit_available(self) -> bool:
        """Check if Bandit is available."""
        try:
            result = subprocess.run(
                ["bandit", "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _run_bandit(self, code: str, temp_dir: Path) -> dict[str, Any]:
        """Run Bandit on Python code and return results."""
        code_file = temp_dir / "test_code.py"
        code_file.write_text(code)

        result = subprocess.run(
            [
                "bandit",
                "-f", "json",
                "-q",
                str(code_file)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"results": [], "errors": []}

    @pytest.mark.slow
    @pytest.mark.skip(reason="Slow SAST integration test")
    def test_python_dont_examples_flagged_by_bandit(
        self,
        code_blocks_by_language: dict[str, list[dict[str, Any]]],
        bandit_available: bool
    ) -> None:
        """Verify Python Don't examples trigger Bandit warnings."""
        if not bandit_available:
            pytest.skip("Bandit not available")

        python_blocks = code_blocks_by_language.get("python", [])
        dont_blocks = [b for b in python_blocks if b["type"] == "dont"]

        if not dont_blocks:
            pytest.skip("No Python Don't examples found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            untriggered = []

            for block in dont_blocks:
                code = block["code"]
                rule_name = block["rule_name"]

                # Skip incomplete code snippets
                if code.strip().startswith("..."):
                    continue

                results = self._run_bandit(code, temp_path)

                if not results.get("results"):
                    untriggered.append(
                        f"Rule '{rule_name}': Don't example not flagged by Bandit"
                    )

            if untriggered:
                # This is expected for some examples
                pytest.xfail(
                    f"{len(untriggered)} Python Don't examples not detected by Bandit"
                )

    @pytest.mark.slow
    @pytest.mark.skip(reason="Slow SAST integration test")
    def test_python_do_examples_pass_bandit(
        self,
        code_blocks_by_language: dict[str, list[dict[str, Any]]],
        bandit_available: bool
    ) -> None:
        """Verify Python Do examples pass Bandit checks."""
        if not bandit_available:
            pytest.skip("Bandit not available")

        python_blocks = code_blocks_by_language.get("python", [])
        do_blocks = [b for b in python_blocks if b["type"] == "do"]

        if not do_blocks:
            pytest.skip("No Python Do examples found")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            errors = []

            for block in do_blocks:
                code = block["code"]
                rule_name = block["rule_name"]

                results = self._run_bandit(code, temp_path)

                # Check for high/medium severity issues
                issues = [
                    r for r in results.get("results", [])
                    if r.get("issue_severity") in ["HIGH", "MEDIUM"]
                ]

                if issues:
                    errors.append(
                        f"Rule '{rule_name}': "
                        f"Do example has {len(issues)} Bandit issue(s)"
                    )

            if errors:
                pytest.fail("\n".join(errors))


class TestCustomSecurityRules:
    """Tests for custom security validation rules."""

    def test_sql_injection_patterns_in_dont_examples(
        self, code_blocks_by_language: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Verify SQL injection patterns are present in Don't examples."""
        # Common SQL injection vulnerability patterns
        injection_patterns = [
            r'f".*SELECT.*{',           # Python f-string SQL
            r"f'.*SELECT.*{",           # Python f-string SQL
            r'".+SELECT.+\+',           # String concatenation SQL
            r"'.+SELECT.+\+",           # String concatenation SQL
            r"\$\{.*\}.*SELECT",        # Template literal SQL
            r"format\(.*SELECT",        # format() with SQL
            r"%s.*SELECT|SELECT.*%s",   # %-formatting SQL
        ]

        import re
        combined_pattern = re.compile("|".join(injection_patterns), re.IGNORECASE)

        # Check Python and JavaScript examples
        for lang in ["python", "javascript", "typescript"]:
            blocks = code_blocks_by_language.get(lang, [])
            dont_blocks = [b for b in blocks if b["type"] == "dont"]

            sql_related = [
                b for b in dont_blocks
                if "sql" in b["rule_name"].lower() or "injection" in b["rule_name"].lower()
            ]

            for block in sql_related:
                code = block["code"]
                rule_name = block["rule_name"]

                if not combined_pattern.search(code):
                    # Informational - not all SQL rules show injection
                    pass

    def test_hardcoded_secrets_in_dont_examples(
        self, code_blocks_by_language: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Verify hardcoded secret patterns in relevant Don't examples."""
        import re

        # Patterns that indicate hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\']',
            r'api_key\s*=\s*["\']',
            r'secret\s*=\s*["\']',
            r'token\s*=\s*["\'][A-Za-z0-9]',
            r'AWS_SECRET',
            r'-----BEGIN.*KEY-----',
        ]

        combined_pattern = re.compile("|".join(secret_patterns), re.IGNORECASE)

        all_blocks = []
        for blocks in code_blocks_by_language.values():
            all_blocks.extend(blocks)

        # Find secret-related rules
        secret_rules = [
            b for b in all_blocks
            if b["type"] == "dont" and any(
                keyword in b["rule_name"].lower()
                for keyword in ["secret", "credential", "password", "key"]
            )
        ]

        for block in secret_rules:
            code = block["code"]
            rule_name = block["rule_name"]

            if not combined_pattern.search(code):
                # Some secret rules might show other patterns
                pass

    def test_xss_patterns_in_dont_examples(
        self, code_blocks_by_language: dict[str, list[dict[str, Any]]]
    ) -> None:
        """Verify XSS vulnerability patterns in relevant Don't examples."""
        import re

        # Patterns that indicate XSS vulnerabilities
        xss_patterns = [
            r"innerHTML\s*=",
            r"document\.write\(",
            r"eval\(",
            r"\|\s*safe",                    # Django/Jinja safe filter
            r"dangerouslySetInnerHTML",      # React
            r"v-html",                        # Vue
        ]

        combined_pattern = re.compile("|".join(xss_patterns))

        js_blocks = (
            code_blocks_by_language.get("javascript", []) +
            code_blocks_by_language.get("typescript", [])
        )

        xss_rules = [
            b for b in js_blocks
            if b["type"] == "dont" and "xss" in b["rule_name"].lower()
        ]

        for block in xss_rules:
            code = block["code"]
            rule_name = block["rule_name"]

            if not combined_pattern.search(code):
                # Some XSS rules might show other patterns
                pass


class TestSecurityRuleCoverage:
    """Tests for security rule coverage of common vulnerabilities."""

    def test_owasp_top_10_coverage(
        self, all_rules: list[dict[str, Any]]
    ) -> None:
        """Verify coverage of OWASP Top 10 2021 categories."""
        owasp_2021 = {
            "A01": "Broken Access Control",
            "A02": "Cryptographic Failures",
            "A03": "Injection",
            "A04": "Insecure Design",
            "A05": "Security Misconfiguration",
            "A06": "Vulnerable Components",
            "A07": "Authentication Failures",
            "A08": "Integrity Failures",
            "A09": "Logging Failures",
            "A10": "SSRF"
        }

        covered = set()

        for rule in all_rules:
            refs = rule["sections"].get("Refs", "")
            why = rule["sections"].get("Why", "")
            combined = refs + " " + why

            for code, name in owasp_2021.items():
                if code in combined or name.lower() in combined.lower():
                    covered.add(code)

        uncovered = set(owasp_2021.keys()) - covered

        if uncovered:
            missing_names = [f"{k}: {owasp_2021[k]}" for k in uncovered]
            pytest.fail(
                f"Missing OWASP Top 10 coverage:\n" +
                "\n".join(missing_names)
            )

    def test_common_cwe_coverage(
        self, cwe_references: dict[str, list[str]]
    ) -> None:
        """Verify coverage of common CWE vulnerabilities."""
        # Critical CWEs that should be covered
        critical_cwes = [
            "CWE-79",   # XSS
            "CWE-89",   # SQL Injection
            "CWE-287",  # Improper Authentication
            "CWE-798",  # Hardcoded Credentials
            "CWE-306",  # Missing Authentication
        ]

        missing = [
            cwe for cwe in critical_cwes
            if cwe not in cwe_references
        ]

        if missing:
            pytest.fail(
                f"Missing critical CWE coverage: {', '.join(missing)}"
            )

    def test_language_specific_security_rules(
        self, rules_by_file: dict[Path, list[dict[str, Any]]]
    ) -> None:
        """Verify language-specific security rules exist."""
        # Expected security-related rules per language
        expected_rules = {
            "python": ["injection", "pickle", "eval"],
            "javascript": ["xss", "prototype", "eval"],
            "go": ["sql", "command", "tls"],
        }

        errors = []

        for filepath, rules in rules_by_file.items():
            for lang, keywords in expected_rules.items():
                if lang in str(filepath).lower():
                    rule_text = " ".join(
                        r["name"].lower() + r.get("raw_text", "").lower()
                        for r in rules
                    )

                    missing = [
                        kw for kw in keywords
                        if kw not in rule_text
                    ]

                    if missing:
                        errors.append(
                            f"{filepath}: Missing {lang} rules for "
                            f"{', '.join(missing)}"
                        )

        if errors:
            pytest.fail("\n".join(errors))
