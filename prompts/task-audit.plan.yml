# Google Gemini Assessment Recommendation Plan

This plan outlines concrete steps to address the recommendations from the Google Gemini assessment of the `mcp-servers/policy-mcp-server` project. The goal is to elevate the project to a high-quality, production-grade system by refining code quality, observability, policy integration, testing, and documentation.

## 0. Pre-requites
- Ensure that you are in the correct project directory: /workspaces/mcp-servers/policy-mcp-server
   - Make sure that when you are issuing or running commands, you know where you are running the commands from
- Create new git branch so that you are not modifying the existing code base
   - new git branch: 'feature/gemini-recommendation'
   - if there is a conflict in creating new branch, then use 'git stash' to save and switch over.
- Ensure that you are using Asrtal's 'uv' command for pip install and creating virtual env.
- Make sure you are using virtual env and confirm it.
- After installing all packages needed for the project, lock or pin the requirements.txt or uv.lock

**Completed: 2025-06-04  (by GitHub Copilot)**

## 1. Refactor Imports and Packaging
- Standardize Python imports to avoid dynamic path manipulation (e.g., `sys.path.append`, `importlib.util.spec_from_file_location`).
- Restructure the project as a proper Python package:
  - Ensure all modules are importable via standard Python imports.
  - Use a complete `pyproject.toml` or `setup.py` to define the package and entry points.
  - Support editable installs (`pip install -e .`).
  - Remove all ad-hoc import hacks from code and tests.
- Ensure `__init__.py` files are present and correct in all packages.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 2. Revisit Async Handling
- Review the use of async code in synchronous contexts (notably in `src/server.py`).
- If `fastmcp` is synchronous, document and isolate async workarounds (e.g., `asyncio.run_until_complete`).
- Investigate if `fastmcp` can support async natively; if so, refactor to use async/await throughout.
- Minimize complexity and potential issues from mixing sync/async code.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 3. Enhance OpenTelemetry (OTEL) Instrumentation
- Decouple tracing from the `log_around` decorator; use explicit tracing decorators where needed.
- Add custom attributes to OTEL spans for XAI/auditability (e.g., request ID, user ID, policy decision).
- Implement custom metrics (e.g., counters for policy evaluations, histograms for latency, error rates).
- Make provider setup explicit (e.g., `metrics.set_meter_provider`).
- Ensure graceful degradation is robust and well-tested.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 4. Clarify and Strengthen OPA Policy Mechanism
- Ensure a valid `policy.rego` file is present and used by OPA.
- Clarify the relationship between `policy.json` (data) and `policy.rego` (policy logic).
- Update documentation and `docker-compose-opa.yaml` to reflect the correct policy/data setup.
- Improve error handling and resilience in OPA integration:
  - Catch specific exceptions (e.g., network errors, timeouts).
  - Consider retry logic or circuit breakers for OPA calls.
  - Apply graceful degradation principles if OPA is unavailable.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 5. Standardize and Improve Testing
- Adopt a single testing style (pytest-native: plain functions, direct `assert` statements).
- Refactor tests that use class-based or mixed styles to follow pytest conventions.
- Increase test coverage, especially for error paths and edge cases (e.g., OPA/OTEL failures, config errors).
- Add tests for custom metrics and tracing.
- Ensure tests do not rely on dynamic imports or path hacks.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 6. Robust Error Handling
- Replace broad `except Exception` blocks with specific exception handling.
- Log errors at appropriate levels (info, warning, error, debug).
- Review and adjust the `log_around` decorator to avoid noisy or unnecessary warnings (e.g., downgrade "NO TRACE FOUND" to debug).

**Completed: 2025-06-04  (by GitHub Copilot)**

## 7. Documentation and Developer Experience
- Add a dedicated `.env.example` file at the project root for easy setup.
- Update `README.md` to:
  - Reflect any changes in project structure, configuration, and setup.
  - Clarify OPA policy/data requirements and OTEL instrumentation.
  - Remove or update platform-specific paths (e.g., Windows paths in VS Code settings).
- Ensure all code files have appropriate headers (author, date, AI warning).

**Completed: 2025-06-04  (by GitHub Copilot)**

## 8. Security and Best Practices
- Review and document security practices (e.g., PoLP, secure OPA/OTEL communication).
- Consider more robust policy enforcement mechanisms (beyond simple word lists).
- Ensure policies do not introduce security vulnerabilities.

**Completed: 2025-06-04  (by GitHub Copilot)**

## 9. Project Scaffolding and Maintenance
- Update or document the scaffolding script to match the improved project structure.
- Ensure generated files (e.g., `README.md`) are comprehensive and up-to-date.

**Completed: 2025-06-04  (by GitHub Copilot)**

---

**By following this plan, the project will address all recommendations from the Google Gemini assessment and move closer to enterprise-grade quality, maintainability, and compliance.**
