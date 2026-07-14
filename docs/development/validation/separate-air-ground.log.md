# Separate air and ground combat validation failure

apply status: 1
test status: 0

## Apply log
```text
Traceback (most recent call last):
  File "/home/runner/work/triplea-rebased/triplea-rebased/tools/apply_separate_air_ground_combat.py", line 463, in <module>
    replace(
  File "/home/runner/work/triplea-rebased/triplea-rebased/tools/apply_separate_air_ground_combat.py", line 19, in replace
    raise RuntimeError(f"replacement marker not found in {path}: {old[:160]!r}")
RuntimeError: replacement marker not found in docs/development/small-front-roadmap.md: '## 9. Separate air and ground combat\n\n- distinct air-battle and ground-battle scheduling\n- dependency ordering: air battle before ground battle\n- aircraft canno'
```

## Gradle log
```text
```
