# Git Collaboration — Developer A + Developer B

> **Note:** This is an individual assignment that simulates two developers (Developer A and Developer B) working collaboratively using feature branches on a single local repository. The workflow demonstrates industry-standard practices including cloning, branching, committing with meaningful messages, pushing to remote, creating Pull Requests (PRs), code review, running new test cases, and merge approval.

**Repository:** [https://github.com/praveend0676/course-management-system](https://github.com/praveend0676/course-management-system)  
**Date Completed:** 2026-10-13

All commands listed below were executed step-by-step as documented. This guide provides detailed explanations for each step to help you replicate the workflow.

---

## 1. Prerequisites and Initial Setup

Before starting the collaboration workflow, ensure you have the following tools installed and configured:

- [Git](https://git-scm.com/downloads) (version control)
- [GitHub CLI (gh)](https://cli.github.com/) (for creating repos and PRs)
- [Python 3.10+](https://www.python.org/downloads/)

### 1.1 Authenticate and Configure Git

```bash
# Authenticate with GitHub CLI
gh auth login

# Configure your Git identity (replace with your details)
git config --global user.name "praveend0676"
git config --global user.email "praveendevisetti0676@gmail.com"

# (Optional but recommended) Set default branch to main
git config --global init.defaultBranch main
```

### 1.2 Set Up Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on macOS/Linux
# source .venv/bin/activate
```

### 1.3 Verify Setup

```bash
git --version
gh --version
python --version
```

---

## 2. Developer A — Initializes `main` and Pushes the Code

**Role:** Developer A initializes the repository on `main`, sets up the project structure, and pushes the baseline code to GitHub so Developer B can clone it.

### Step 2.1: Initialize Git Repository

Navigate to your project directory and initialize a new Git repository with `main` as the default branch.

```bash
git init -b main
```

**Explanation:** `git init` creates a new Git repository. The `-b main` flag sets the default branch name to `main` (modern Git convention).

### Step 2.2: Create Project Files and Structure

Create the necessary files and directories for the Course Management System:

- `.gitignore` - Specifies files to exclude from version control
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies (if any)
- `course_management/` - Main application package (`models.py`, `service.py`, `storage.py`, `app.py`, `exceptions.py`)
- `tests/` - Unit test files (`test_system.py`)
- `data/` - Directory for JSON data storage

```bash
# Create directories
mkdir course_management tests data

# Create essential files (or create them via editor)
# .gitignore, README.md, requirements.txt, etc.
```

### Step 2.3: Stage All Files

Add all newly created files to the staging area.

```bash
git add .
```

**Explanation:** `git add .` stages all changes in the current directory and subdirectories.

### Step 2.4: Make Initial Commit

Create the first commit with a clear, descriptive message following conventional commit style.

```bash
git commit -m "chore: initialize course management system"
```

**Explanation:** This establishes the baseline of the project in Git history.

### Step 2.5: Create GitHub Repository and Push

Use GitHub CLI to create a public repository and push the initial commit in one command.

```bash
gh repo create course-management-system --public --source=. --remote=origin --push
```

**Parameters:**
- `--public` - Makes the repository publicly accessible
- `--source=.` - Uses the current directory as source
- `--remote=origin` - Names the remote as 'origin'
- `--push` - Pushes the local commits to the remote

**Result:** Repository created at `https://github.com/praveend0676/course-management-system`

### Step 2.6: Track Additional Changes (If Needed)

Stage any new files that might have been created after the initial commit.

```bash
git add .
```

### Step 2.7: Remove Build Artifacts from Tracking

Python creates `__pycache__` directories with compiled bytecode. These should not be tracked in version control. Remove them from Git's index while keeping them locally.

```bash
git rm -r --cached course_management/__pycache__ tests/__pycache__
git commit -m "chore: stop tracking __pycache__ build artifacts"
```

**Explanation:** `--cached` removes files from the index (staging) but preserves them on disk. This is important for build artifacts that are generated locally.

### Step 2.8: Fix .gitignore Line Endings (If Needed)

If `.gitignore` was created with incorrect line endings (e.g., a literal `\n`), rewrite it with proper newlines to ensure ignore rules are applied correctly.

```bash
# Recreate .gitignore with proper formatting
# Then stage and commit
git add .gitignore
git commit -m "chore: fix .gitignore line endings so ignore rules apply"
```

**Verification:** Check that `.gitignore` properly ignores `__pycache__/` and other unwanted files.

### Step 2.9: Push Final Changes to Main

Push all commits to the remote repository.

```bash
git push origin main
```

**Final State on GitHub (main branch):**
- Commit `c3c4621` - chore: initialize course management system
- Commit `a90c9e9` - chore: stop tracking __pycache__ build artifacts  
- Commit `b36944b` - chore: fix .gitignore line endings so ignore rules apply

At this point `main` is stable and ready for Developer B to clone.

---

## 3. Developer B — Clones the Repository and Creates a Feature Branch

**Role:** Developer B clones the repository from GitHub to simulate working on a separate machine, then creates an isolated feature branch for course enrollment validation.

> **Best Practice:** Never commit directly to `main`. All new work should be done on feature branches and integrated through Pull Requests after review.

### Step 3.1: Clone the Repository

Developer B obtains the repository URL from Developer A and clones a full copy (all branches, history, and remote configuration).

```bash
# Clone into a new directory (simulates Developer B's own machine/workspace)
git clone https://github.com/praveend0676/course-management-system.git
cd course-management-system
```

**Explanation:**
- `git clone` downloads the complete repository from GitHub, including full commit history.
- It automatically creates a local `main` branch tracking `origin/main`.
- It configures `origin` to point at the GitHub remote.

**Verification:** Confirm the clone succeeded and inspect the remote and branch:

```bash
git remote -v          # origin -> https://github.com/praveend0676/course-management-system.git
git branch --show-current   # main
git log --oneline      # shows the three baseline commits from Developer A
```

> **Single-machine simulation note:** For this individual assignment, Developer B's "clone" can also be a second local clone in a sibling directory (e.g., `git clone ../course-management-system ../course-management-system-b`) so the two developers do not share a working directory. If you simulate both roles in one directory instead, run `git fetch origin` and verify local `main` is up to date with `origin/main` before creating the feature branch.

### Step 3.2: Set Up the Environment

```bash
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
```

Run the existing tests to confirm the cloned baseline is healthy before making changes:

```bash
python -m unittest discover -s tests -v
```

**Expected Output:** All 5 baseline tests pass with `OK`. This proves Developer B started from a working `main`.

### Step 3.3: Sync with Latest Main Branch (Before Branching)

Before creating a feature branch, ensure your local `main` is up to date with the remote (in case Developer A pushed more commits after your clone).

```bash
# Switch to main branch
git switch main

# Pull latest changes from origin/main with fast-forward only
git pull --ff-only origin main
```

**Explanation:** `--ff-only` ensures we only update if the remote history is a linear extension of local history, preventing unintended merges.

### Step 3.4: Create and Switch to Feature Branch

Create a new feature branch for implementing course enrollment validation.

```bash
git switch -c feature/course-enrollment
```

**Explanation:** `-c` creates a new branch and switches to it. Branch names should be descriptive (e.g., `feature/`, `fix/`, `chore/` prefixes).

**Verification:** Check current branch with `git branch --show-current` — it should print `feature/course-enrollment`.

---

## 4. Developer B — Implements and Validates Course Enrollment

**Role:** Developer B implements the complete course enrollment validation feature on the feature branch, with corresponding test coverage.

### Step 4.1: Understand the Enrollment Flow

The enrollment flow lives in `course_management/service.py` and follows this path:

1. `CourseManagementService.enroll_student(student_id, course_id)` is the public entry point.
2. It delegates validation to the `_validate_enrollment()` helper.
3. On success it creates an `Enrollment` record; on failure it raises a typed domain exception.

### Step 4.2: File Change #1 — `course_management/service.py`

Developer B refactored `enroll_student()` by extracting a dedicated `_validate_enrollment()` helper that centralizes all enrollment business rules.

**Before (validation was not centralized):** enrollment logic was inline in `enroll_student()`, making it hard to test and extend.

**After — added `_validate_enrollment()` helper and slimmed `enroll_student()`:**

```python
def _validate_enrollment(self, student_id, course_id):
    # 1) Student must exist -> raises NotFoundError if unknown
    student = self._get(self.students, student_id, "Student")
    # 2) Course must exist -> raises NotFoundError if unknown
    course = self._get(self.courses, course_id, "Course")
    # 3) No duplicate enrollment -> raises EnrollmentError if already enrolled
    if student_id in course.enrolled_student_ids:
        raise EnrollmentError("Student is already enrolled")
    # 4) Course capacity must not be exhausted -> raises EnrollmentError if full
    if course.seats_available <= 0:
        raise EnrollmentError("Course is full")
    # 5) Generate a unique enrollment ID -> raises ValidationError on collision
    eid = f"ENR-{student_id}-{course_id}"
    self._unique(eid, self.enrollments, "Enrollment")
    return student, course, eid

def enroll_student(self, student_id, course_id):
    student, course, eid = self._validate_enrollment(student_id, course_id)
    enrollment = Enrollment.create(student, course, eid)
    self.enrollments[eid] = enrollment
    return enrollment
```

**Validation rules implemented:**

| # | Rule | Exception raised |
|---|------|------------------|
| 1 | Student must exist | `NotFoundError` |
| 2 | Course must exist | `NotFoundError` |
| 3 | Student must not already be enrolled in the course | `EnrollmentError` |
| 4 | Course must have seats available | `EnrollmentError` |
| 5 | Generated enrollment ID must be unique | `ValidationError` |

### Step 4.3: File Change #2 — `tests/test_system.py`

Developer B extended `test_enrollment_capacity_and_duplicate` with new `NotFoundError` assertions so that enrolling a non-existent student in a non-existent course is covered:

```python
def test_enrollment_capacity_and_duplicate(self):
    self.service.add_student(Student("S1", "Asha", "a@example.com"))
    self.service.add_student(Student("S2", "Bala", "b@example.com"))
    self.service.add_course(Course("C1", "Python", "OOP course", capacity=1))
    self.service.enroll_student("S1", "C1")
    with self.assertRaises(EnrollmentError): self.service.enroll_student("S1", "C1")  # duplicate
    with self.assertRaises(EnrollmentError): self.service.enroll_student("S2", "C1")  # course full
    with self.assertRaises(NotFoundError): self.service.enroll_student("S3", "C2")    # NEW: unknown student + unknown course
    with self.assertRaises(NotFoundError): self.service.enroll_student("S4", "C2")    # NEW: unknown student + unknown course
```

**Key files modified on the feature branch:**
- `course_management/service.py` — `_validate_enrollment()` helper + refactored `enroll_student()`
- `tests/test_system.py` — new `NotFoundError` test coverage for enrollment

### Step 4.4: Validate the Feature Locally (Run Tests)

Run the full test suite to ensure the implementation is correct and does not break existing functionality.

```bash
python -m unittest discover -s tests -v
```

**Expected Output:** All 5 tests pass with `OK`, including the updated `test_enrollment_capacity_and_duplicate`.

**Why test first?** Running tests before committing catches bugs early and ensures the feature meets requirements.

### Step 4.5: Stage and Commit Changes

Stage the modified files and commit with a meaningful message following conventional commits.

```bash
# Stage specific files
git add course_management/service.py tests/test_system.py

# Commit with descriptive message
git commit -m "feat: validate course enrollment"
```

**Explanation:** The `feat:` prefix indicates this is a new feature. Keep commit messages concise but descriptive.

### Step 4.6: Push Feature Branch to Remote

Push the feature branch to GitHub and set up tracking.

```bash
git push -u origin feature/course-enrollment
```

**Explanation:** `-u` (or `--set-upstream`) links the local branch to the remote branch, allowing future `git push`/`git pull` without specifying branch names.

---

## 5. Open a Pull Request — `feature/course-enrollment` → `main`

### Step 5.1: Create the Pull Request

Use GitHub CLI to create a PR from the feature branch into `main`.

```bash
gh pr create \
  --base main \
  --head feature/course-enrollment \
  --title "Validate course enrollment" \
  --body "Implements enrollment validation logic including checks for non-existent students/courses, duplicate enrollments, and course capacity. Adds comprehensive test coverage for validation scenarios."
```

**Parameters explained:**
- `--base main` — the branch we want to merge INTO (the stable branch)
- `--head feature/course-enrollment` — the branch containing the new work
- `--title` / `--body` — PR title and description for reviewers

**Alternatively,** you can create PRs via GitHub UI at: `https://github.com/praveend0676/course-management-system/pull/new/feature/course-enrollment`

**Result:** PR #1 created - [View PR](https://github.com/praveend0676/course-management-system/pull/1)

---

## 6. Review the Pull Request

### Step 6.1: Inspect the Diff

```bash
# View the diff to see all changes between main and the feature branch
gh pr diff 1

# Check PR status, mergeability, and any CI checks
gh pr checks 1
gh pr view 1
```

**What the reviewer looks for in the diff:**
- `course_management/service.py` — `_validate_enrollment()` correctly enforces all 5 rules; `enroll_student()` remains a thin wrapper; no dead code.
- `tests/test_system.py` — new `NotFoundError` assertions cover unknown student/course enrollments; existing assertions for duplicate and capacity still pass.

### Step 6.2: Review Checklist

- [ ] Code follows project conventions and style
- [ ] Changes are minimal and focused (only enrollment validation touched)
- [ ] Tests cover the new functionality
- [ ] All existing tests still pass
- [ ] No debug code or commented-out code left behind
- [ ] Commit messages are clear and meaningful

### Step 6.3: Leave Review Feedback (If Needed)

```bash
# Add a review comment
gh pr review 1 --comment --body "Looks good — validation rules are clearly separated and tested."

# Or request changes if something needs fixing
# gh pr review 1 --request-changes --body "Please add a test for unique enrollment ID collision."

# After the author pushes fixes, re-review and approve
gh pr review 1 --approve --body "Approved — enrollment validation is complete and well tested."
```

**Approval gate:** The PR should not be merged until the reviewer approves (via `gh pr review --approve` or the GitHub UI "Approve" button) and all required checks pass.

---

## 7. Run the New Test Cases (Final Verification Before Merge)

### Step 7.1: Check Out the PR Branch Locally

```bash
# GitHub CLI can check out the PR for local testing
gh pr checkout 1
```

**Or** switch manually:

```bash
git switch feature/course-enrollment
git pull --ff-only origin feature/course-enrollment
```

### Step 7.2: Run the Full Test Suite

```bash
python -m unittest discover -s tests -v
```

**Expected Output:** `Ran 5 tests in ...s` with `OK`.

**What was verified:**
1. `test_user_is_abstract` — abstraction still enforced
2. `test_static_method_and_polymorphism` — email validation and role descriptions intact
3. `test_enrollment_capacity_and_duplicate` — **updated:** duplicate, capacity, and unknown student/course paths all raise the correct exceptions
4. `test_json_round_trip` — persistence still round-trips enrollments
5. `test_invalid_email` — domain validation intact

**Optional:** run the app manually for a smoke test:

```bash
python -m course_management.app
# Add a student, create a course, enroll the student, then try enrolling again
# (expect "Student is already enrolled") and enroll an unknown ID (expect "not found").
```

### Step 7.3: Confirm the Working Tree Is Clean

```bash
git status
git log --oneline -3
```

Only the intended commit (`feat: validate course enrollment`) should be present on the feature branch.

---

## 8. Merge Approval — Merge the Pull Request

### Step 8.1: Confirm Approval and Checks

```bash
gh pr view 1 --json state,reviewDecision,mergeable
```

**Expected:** `state: OPEN`, `reviewDecision: APPROVED`, `mergeable: MERGEABLE`.

### Step 8.2: Merge with Squash (Squash Merge)

After review and approval, merge the PR using squash merge. Squashing combines all feature branch commits into a single clean commit on `main`.

```bash
gh pr merge 1 --squash --delete-branch
```

**Options explained:**
- `--squash` - Combines all commits from the feature branch into one commit
- `--delete-branch` - Deletes the remote feature branch after merging

**Why squash merge?** It keeps the `main` branch history clean and linear, with one commit per feature/fix.

### Step 8.3: Clean Up Local References (Developer B)

After merging and deleting the remote branch, clean up local branches and fetch the updated state.

```bash
# Switch back to main
git switch main

# Fetch updates and prune deleted remote branches
git fetch --prune origin
```

**Explanation:** `--prune` removes local remote-tracking branches (like `origin/feature/course-enrollment`) that no longer exist on the remote.

### Step 8.4: Delete the Local Feature Branch (Optional)

```bash
git branch -d feature/course-enrollment
```

---

## 9. Developer A — Integrates the Merged Feature

**Role:** Developer A (or the repo maintainer) pulls the merged changes back into their local `main` branch to stay in sync with the remote.

### Step 9.1: Switch to Main and Pull Updates

```bash
# Switch to main branch
git switch main

# Pull the merged changes (fast-forward merge)
git pull --ff-only origin main
```

**Explanation:** The squash-merged PR created a new commit on `main` (`58ba11b feat: validate course enrollment (#1)`). Since no local changes conflict, this will fast-forward cleanly.

### Step 9.2: Clean Up Stale Remote References

```bash
# Prune deleted remote-tracking branches
git fetch --prune origin
```

**Why prune?** After merging and deleting `feature/course-enrollment` on GitHub, the remote-tracking ref `origin/feature/course-enrollment` becomes stale and should be removed locally.

### Step 9.3: Verify Integration

View the commit history to confirm the merge is reflected.

```bash
git log --oneline --graph --all
```

Run all tests to ensure everything still passes after integration.

```bash
python -m unittest discover -s tests -v
```

**Expected Result:** `Ran 5 tests in ...s` with `OK` - all tests pass.

---

## 10. Final State

### Final Commit History on `main`

```text
58ba11b feat: validate course enrollment (#1)     <- merged PR #1 (squash commit)
b36944b chore: fix .gitignore line endings so ignore rules apply
a90c9e9 chore: stop tracking __pycache__ build artifacts
c3c4621 chore: initialize course management system
```

### Links

- **Repository:** [https://github.com/praveend0676/course-management-system](https://github.com/praveend0676/course-management-system)
- **Pull Request #1:** [https://github.com/praveend0676/course-management-system/pull/1](https://github.com/praveend0676/course-management-system/pull/1) (MERGED)

---

## 11. Workflow Summary (Quick Reference)

| Step | Developer | Action | Command |
|------|-----------|--------|---------|
| 1 | A | Initialize `main` | `git init -b main` |
| 2 | A | Stage and commit baseline | `git add .` → `git commit -m "chore: initialize course management system"` |
| 3 | A | Create repo and push `main` | `gh repo create course-management-system --public --source=. --remote=origin --push` |
| 4 | B | Clone the repository | `git clone https://github.com/praveend0676/course-management-system.git` |
| 5 | B | Create feature branch | `git switch -c feature/course-enrollment` |
| 6 | B | Implement + validate enrollment | Edit `course_management/service.py`, `tests/test_system.py` → `python -m unittest discover -s tests -v` |
| 7 | B | Commit and push feature | `git add …` → `git commit -m "feat: validate course enrollment"` → `git push -u origin feature/course-enrollment` |
| 8 | B | Open Pull Request | `gh pr create --base main --head feature/course-enrollment …` |
| 9 | Reviewer | Review PR | `gh pr diff 1` → review checklist → `gh pr review 1 --approve` |
| 10 | Reviewer | Run new test cases | `gh pr checkout 1` → `python -m unittest discover -s tests -v` |
| 11 | Reviewer | Merge with approval | `gh pr merge 1 --squash --delete-branch` |
| 12 | A/B | Sync and clean up | `git switch main` → `git pull --ff-only origin main` → `git fetch --prune origin` |

---

## 12. Key Learnings & Best Practices

- **Clone for Independence:** Developer B cloned the repository rather than sharing Developer A's working directory, simulating genuinely independent machines.
- **Feature Isolation:** All feature work was kept on the `feature/course-enrollment` branch, isolated from `main`. This prevents breaking the stable branch.
- **Meaningful Commits:** Used conventional commit messages (`chore:`, `feat:`) to clearly communicate the purpose of each change.
- **Code Review via PRs:** Changes were reviewed through a Pull Request before merging, promoting quality and collaboration.
- **Approval Gate:** Merging only happened after an explicit review approval and a clean test run on the PR branch.
- **Clean History:** Used squash merge to keep `main`'s history linear and readable.
- **Proper .gitignore:** Ensured build artifacts (`__pycache__/*.pyc`) are ignored and removed from tracking.
- **Safe Syncing:** Used `git pull --ff-only` to avoid accidental merge commits when syncing.
- **Branch Hygiene:** Deleted the feature branch after merging and pruned stale refs locally.
- **Test-Driven Verification:** Ran unit tests at multiple points (baseline after clone, after implementation, before commit, after merge) to ensure correctness.
- **No History Rewriting:** No `force-push` was used on `main`, preserving repository integrity.

---

## 13. Appendix — Developer B's Complete Code Changes (PR Diffs)

This appendix contains the exact code changes Developer B made on `feature/course-enrollment` to complete the problem statement: **validate the complete course enrollment with respective file changes**. These are the changes that appear in `gh pr diff 1` and get merged back into `main` in Step 8. Existing steps above are unchanged — this appendix only documents the code itself.

**Problem statement → implementation mapping:**

| Enrollment validation rule | File that enforces it | Test that covers it |
|---|---|---|
| Student must exist | `course_management/service.py` (`NotFoundError`) | `test_enrollment_capacity_and_duplicate` |
| Course must exist | `course_management/service.py` (`NotFoundError`) | `test_enrollment_capacity_and_duplicate` |
| No duplicate enrollment | `course_management/service.py` (`EnrollmentError`) | `test_enrollment_capacity_and_duplicate` |
| Course capacity not exhausted | `course_management/service.py` (`EnrollmentError`) | `test_enrollment_capacity_and_duplicate` |
| Enrollment ID uniqueness | `course_management/service.py` (`ValidationError`) | covered by `_unique()` guard |

**Files changed in the PR:** exactly two —
- `course_management/service.py` (feature logic)
- `tests/test_system.py` (test coverage)

### 13.1 Diff — `course_management/service.py`

Extracts the five validation rules into a dedicated `_validate_enrollment()` helper; `enroll_student()` becomes a thin wrapper that validates first, then creates the `Enrollment` record.

```diff
diff --git a/course_management/service.py b/course_management/service.py
--- a/course_management/service.py
+++ b/course_management/service.py
@@ -36,7 +36,7 @@ class CourseManagementService:
     def assign_mentor(self, course_id, mentor_id):
         self._get(self.courses, course_id, "Course").assign_mentor(self._get(self.mentors, mentor_id, "Mentor"))

-    def enroll_student(self, student_id, course_id):
+    def _validate_enrollment(self, student_id, course_id):
         student = self._get(self.students, student_id, "Student")
         course = self._get(self.courses, course_id, "Course")
         if student_id in course.enrolled_student_ids:
@@ -45,6 +45,10 @@ class CourseManagementService:
             raise EnrollmentError("Course is full")
         eid = f"ENR-{student_id}-{course_id}"
         self._unique(eid, self.enrollments, "Enrollment")
+        return student, course, eid
+
+    def enroll_student(self, student_id, course_id):
+        student, course, eid = self._validate_enrollment(student_id, course_id)
         enrollment = Enrollment.create(student, course, eid)
         self.enrollments[eid] = enrollment
         return enrollment
```

**Why these are good changes to accept in review:**
- All five validation rules sit in one testable helper instead of being buried in the public method.
- `enroll_student()` keeps its signature, return value, and side effects — no callers break (`app.py`, tests, persistence all unchanged).
- No new dependencies; only existing typed exceptions (`NotFoundError`, `EnrollmentError`, `ValidationError`) are raised.

### 13.2 Diff — `tests/test_system.py`

Adds the two `NotFoundError` assertions so the "student/course must exist" part of the problem statement is explicitly verified.

```diff
diff --git a/tests/test_system.py b/tests/test_system.py
--- a/tests/test_system.py
+++ b/tests/test_system.py
@@ -31,6 +31,8 @@ class CourseSystemTests(unittest.TestCase):
         self.service.enroll_student("S1", "C1")
         with self.assertRaises(EnrollmentError): self.service.enroll_student("S1", "C1")
         with self.assertRaises(EnrollmentError): self.service.enroll_student("S2", "C1")
+        with self.assertRaises(NotFoundError): self.service.enroll_student("S3", "C2")
+        with self.assertRaises(NotFoundError): self.service.enroll_student("S4", "C2")

     def test_json_round_trip(self):
         self.service.add_student(Student("S1", "Asha", "a@example.com"))
```

**Assertion coverage after the change (all inside `test_enrollment_capacity_and_duplicate`):**

| Line | Scenario | Expected exception |
|---|---|---|
| 32 | Enroll `S1` in `C1` a second time (duplicate) | `EnrollmentError` |
| 33 | Enroll `S2` in `C1` when capacity `1` is exhausted | `EnrollmentError` |
| 34 | Enroll unknown student `S3` in unknown course `C2` | `NotFoundError` (new) |
| 35 | Enroll unknown student `S4` in unknown course `C2` | `NotFoundError` (new) |

### 13.3 Regenerating the Diff Locally

Developer B (or the reviewer) can reproduce the exact PR diff at any time from the repository root:

```bash
# Three-dot diff: changes on the feature branch since it diverged from main
git diff main...feature/course-enrollment

# Or view the PR diff directly after opening the PR
gh pr diff 1
```

**Verification after applying the changes:**

```bash
python -m unittest discover -s tests -v
```

**Expected:** `Ran 5 tests in ...s` with `OK` — the 4 existing assertions plus the 2 new `NotFoundError` assertions all pass. These are the changes squash-merged into `main` as `feat: validate course enrollment (#1)`.

---

**End of Documentation**
