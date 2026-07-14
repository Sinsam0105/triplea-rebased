# Separate air and ground combat validation failure

apply status: 0
test status: 1

## Apply log
```text
```

## Gradle log
```text
Fetching distribution.
Downloading https://services.gradle.org/distributions/gradle-9.6.1-all.zip
......................10%.......................20%.......................30%.......................40%.......................50%.......................60%......................70%.......................80%.......................90%.......................100%

Welcome to Gradle 9.6.1!

Here are the highlights of this release:
 - Improved Configuration Cache hit rates
 - Additional CLI rendering options
 - Important project hierarchy lookup deprecations

For more details see https://docs.gradle.org/9.6.1/release-notes.html

Starting a Gradle Daemon (subsequent builds will be faster)
Calculating task graph as no cached configuration is available for tasks: spotlessApply :game-core:test :game-headless:test
> Task :build-logic:failure-summary-plugin:compileJava
> Task :build-logic:failure-summary-plugin:pluginDescriptors
> Task :build-logic:failure-summary-plugin:processResources
> Task :build-logic:failure-summary-plugin:classes
> Task :build-logic:failure-summary-plugin:jar
> Task :build-logic:triplea-test-conventions:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :build-logic:triplea-base-project:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :build-logic:triplea-java-library:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :build-logic:triplea-java-library:extractPrecompiledScriptPluginPlugins
> Task :build-logic:triplea-base-project:extractPrecompiledScriptPluginPlugins
> Task :build-logic:triplea-base-project:generateScriptPluginAdapters
> Task :build-logic:triplea-java-library:generateScriptPluginAdapters
> Task :build-logic:triplea-java-library:pluginDescriptors
> Task :build-logic:triplea-base-project:pluginDescriptors
> Task :build-logic:triplea-java-library:processResources
> Task :build-logic:triplea-base-project:processResources
> Task :build-logic:triplea-test-conventions:generateExternalPluginSpecBuilders
> Task :build-logic:triplea-test-conventions:extractPrecompiledScriptPluginPlugins
> Task :build-logic:triplea-test-conventions:generateScriptPluginAdapters
> Task :build-logic:triplea-test-conventions:pluginDescriptors
> Task :build-logic:triplea-test-conventions:processResources
> Task :build-logic:triplea-test-conventions:compilePluginsBlocks
> Task :build-logic:triplea-test-conventions:generatePrecompiledScriptPluginAccessors
> Task :build-logic:triplea-test-conventions:compileKotlin
> Task :build-logic:triplea-test-conventions:compileJava NO-SOURCE
> Task :build-logic:triplea-test-conventions:classes
> Task :build-logic:triplea-test-conventions:jar
> Task :build-logic:triplea-base-project:generateExternalPluginSpecBuilders FROM-CACHE
> Task :build-logic:triplea-base-project:compilePluginsBlocks
> Task :build-logic:triplea-base-project:generatePrecompiledScriptPluginAccessors
> Task :build-logic:triplea-base-project:compileKotlin
> Task :build-logic:triplea-base-project:compileJava NO-SOURCE
> Task :build-logic:triplea-base-project:classes
> Task :build-logic:triplea-base-project:jar
> Task :build-logic:triplea-java-library:generateExternalPluginSpecBuilders
> Task :build-logic:triplea-java-library:compilePluginsBlocks
> Task :build-logic:triplea-java-library:generatePrecompiledScriptPluginAccessors
> Task :build-logic:triplea-java-library:compileKotlin
> Task :build-logic:triplea-java-library:compileJava NO-SOURCE
> Task :build-logic:triplea-java-library:classes
> Task :build-logic:triplea-java-library:jar
> Task :build-logic:triplea-published-library:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :build-logic:triplea-published-library:generateExternalPluginSpecBuilders FROM-CACHE
> Task :build-logic:triplea-published-library:extractPrecompiledScriptPluginPlugins
> Task :build-logic:triplea-published-library:generateScriptPluginAdapters
> Task :build-logic:triplea-published-library:pluginDescriptors
> Task :build-logic:triplea-published-library:processResources
> Task :build-logic:triplea-published-library:compilePluginsBlocks
> Task :build-logic:triplea-published-library:generatePrecompiledScriptPluginAccessors
> Task :build-logic:triplea-published-library:compileKotlin
> Task :build-logic:triplea-published-library:compileJava NO-SOURCE
> Task :build-logic:triplea-published-library:classes
> Task :build-logic:triplea-published-library:jar
> Task :game-core:processResources
> Task :spotlessInternalRegisterDependencies
> Task :ai:spotlessAllFiles
> Task :ai:spotlessAllFilesApply
> Task :game-core:processTestFixturesResources
> Task :domain-data:spotlessAllFiles
> Task :domain-data:spotlessAllFilesApply
> Task :domain-data:spotlessJava
> Task :domain-data:spotlessJavaApply
> Task :domain-data:spotlessApply
> Task :feign-common:spotlessAllFiles
> Task :feign-common:spotlessAllFilesApply
> Task :feign-common:spotlessJava
> Task :feign-common:spotlessJavaApply
> Task :feign-common:spotlessApply
> Task :game-core:spotlessAllFiles
> Task :game-core:spotlessAllFilesApply
> Task :ai:spotlessJava
> Task :ai:spotlessJavaApply
> Task :ai:spotlessApply
> Task :game-headed:spotlessAllFiles
> Task :game-headed:spotlessAllFilesApply
> Task :java-extras:compileJava
> Task :game-headless:spotlessAllFiles
> Task :lobby-client-data:compileJava
> Task :game-headless:spotlessAllFilesApply
> Task :game-relay-server:spotlessAllFiles
> Task :game-relay-server:spotlessAllFilesApply
> Task :game-relay-server:spotlessJava
> Task :game-relay-server:spotlessJavaApply
> Task :game-relay-server:spotlessApply
> Task :java-extras:spotlessAllFiles
> Task :java-extras:spotlessAllFilesApply
> Task :game-headless:spotlessJava
> Task :game-headless:spotlessJavaApply
> Task :game-headless:spotlessApply
> Task :lobby-client:spotlessAllFiles
> Task :lobby-client:spotlessAllFilesApply
> Task :lobby-client:spotlessJava
> Task :lobby-client:spotlessJavaApply
> Task :lobby-client:spotlessApply
> Task :lobby-client-data:spotlessAllFiles
> Task :lobby-client-data:spotlessAllFilesApply
> Task :lobby-client-data:spotlessJava
> Task :lobby-client-data:spotlessJavaApply
> Task :lobby-client-data:spotlessApply
> Task :map-data:spotlessAllFiles
> Task :map-data:spotlessAllFilesApply
> Task :java-extras:spotlessJava
> Task :java-extras:spotlessJavaApply
> Task :java-extras:spotlessApply
> Task :smoke-testing:spotlessAllFiles
> Task :smoke-testing:spotlessAllFilesApply
> Task :smoke-testing:spotlessJava
> Task :smoke-testing:spotlessJavaApply
> Task :smoke-testing:spotlessApply
> Task :swing-lib:spotlessAllFiles
> Task :swing-lib:spotlessAllFilesApply
> Task :map-data:spotlessJava
> Task :map-data:spotlessJavaApply
> Task :map-data:spotlessApply
> Task :swing-lib-test-support:spotlessAllFiles
> Task :swing-lib-test-support:spotlessAllFilesApply
> Task :swing-lib-test-support:spotlessJava
> Task :swing-lib-test-support:spotlessJavaApply
> Task :swing-lib-test-support:spotlessApply
> Task :test-common:spotlessAllFiles
> Task :test-common:spotlessAllFilesApply
> Task :test-common:spotlessJava
> Task :test-common:spotlessJavaApply
> Task :test-common:spotlessApply
> Task :websocket-client:spotlessAllFiles
> Task :websocket-client:spotlessAllFilesApply
> Task :websocket-client:spotlessJava
> Task :websocket-client:spotlessJavaApply
> Task :websocket-client:spotlessApply
> Task :websocket-server:spotlessAllFiles
> Task :websocket-server:spotlessAllFilesApply
> Task :websocket-server:spotlessJava
> Task :websocket-server:spotlessJavaApply
> Task :websocket-server:spotlessApply
> Task :xml-reader:spotlessAllFiles
> Task :xml-reader:spotlessAllFilesApply
> Task :xml-reader:spotlessJava
> Task :xml-reader:spotlessJavaApply
> Task :xml-reader:spotlessApply
> Task :swing-lib:spotlessJava
> Task :swing-lib:spotlessJavaApply
> Task :swing-lib:spotlessApply
> Task :domain-data:compileJava
> Task :websocket-client:compileJava

> Task :feign-common:compileJava
Note: /home/runner/work/triplea-rebased/triplea-rebased/lib/feign-common/src/main/java/org/triplea/http/client/HttpClient.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :xml-reader:compileJava
> Task :websocket-server:compileJava
> Task :game-headed:spotlessJava
> Task :game-headed:spotlessJavaApply
> Task :game-headed:spotlessApply
> Task :lobby-client:compileJava
> Task :game-relay-server:compileJava
> Task :domain-data:processResources NO-SOURCE
> Task :domain-data:classes
> Task :domain-data:jar
> Task :feign-common:processResources NO-SOURCE
> Task :feign-common:classes
> Task :feign-common:jar

> Task :map-data:compileJava
Note: /home/runner/work/triplea-rebased/triplea-rebased/game-app/map-data/src/main/java/org/triplea/map/description/file/MapDescriptionYamlGenerator.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :game-core:processTestResources
> Task :game-relay-server:processResources NO-SOURCE
> Task :game-relay-server:classes
> Task :game-relay-server:jar
> Task :java-extras:processResources NO-SOURCE
> Task :java-extras:classes

> Task :test-common:compileJava
Note: /home/runner/work/triplea-rebased/triplea-rebased/lib/test-common/src/main/java/org/triplea/test/common/JsonUtil.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :java-extras:jar
> Task :lobby-client:processResources NO-SOURCE
> Task :lobby-client:classes
> Task :lobby-client:jar
> Task :lobby-client-data:processResources NO-SOURCE
> Task :lobby-client-data:classes
> Task :lobby-client-data:jar
> Task :map-data:processResources NO-SOURCE
> Task :map-data:classes
> Task :map-data:jar
> Task :swing-lib:processResources NO-SOURCE
> Task :swing-lib-test-support:processResources NO-SOURCE
> Task :test-common:processResources
> Task :websocket-client:processResources NO-SOURCE
> Task :websocket-client:classes
> Task :websocket-client:jar
> Task :websocket-server:processResources NO-SOURCE
> Task :websocket-server:classes
> Task :websocket-server:jar
> Task :xml-reader:processResources NO-SOURCE
> Task :xml-reader:classes
> Task :xml-reader:jar
> Task :ai:processResources NO-SOURCE
> Task :game-headless:processResources
> Task :game-headless:processTestResources NO-SOURCE
> Task :swing-lib:compileJava
> Task :swing-lib:classes
> Task :swing-lib:jar
> Task :test-common:classes
> Task :test-common:jar
> Task :game-core:spotlessJava
> Task :swing-lib-test-support:compileJava
> Task :swing-lib-test-support:classes
> Task :swing-lib-test-support:jar

> Task :game-core:compileJava
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :game-core:classes
> Task :game-core:jar
> Task :game-core:compileTestFixturesJava
> Task :game-core:testFixturesClasses
> Task :game-core:testFixturesJar
> Task :ai:compileJava
> Task :ai:classes
> Task :ai:jar
> Task :game-headless:compileJava
> Task :game-headless:classes
> Task :game-headless:compileTestJava
> Task :game-headless:testClasses

> Task :game-core:compileTestJava
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: Some input files use unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.

> Task :game-core:testClasses
> Task :game-headless:test
> Task :game-core:test

CombatDomainParticipantsTest > separatedRuleRemovesEnemyAircraftFromGroundDefense() FAILED
    java.lang.NullPointerException: Cannot invoke "games.strategy.engine.data.GameData.getRelationshipTracker()" because the return value of "games.strategy.engine.data.GamePlayer.getData()" is null
        at games.strategy.engine.data.GamePlayer.isAtWar(GamePlayer.java:247)
        at games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest.setUp(CombatDomainParticipantsTest.java:27)

CombatDomainParticipantsTest > infrastructureAloneDoesNotCreateGroundCombat() FAILED
    java.lang.NullPointerException: Cannot invoke "games.strategy.engine.data.GameData.getRelationshipTracker()" because the return value of "games.strategy.engine.data.GamePlayer.getData()" is null
        at games.strategy.engine.data.GamePlayer.isAtWar(GamePlayer.java:247)
        at games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest.setUp(CombatDomainParticipantsTest.java:27)

CombatDomainParticipantsTest > legacyRuleKeepsAircraftInTheNormalBattle() FAILED
    java.lang.NullPointerException: Cannot invoke "games.strategy.engine.data.GameData.getRelationshipTracker()" because the return value of "games.strategy.engine.data.GamePlayer.getData()" is null
        at games.strategy.engine.data.GamePlayer.isAtWar(GamePlayer.java:247)
        at games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest.setUp(CombatDomainParticipantsTest.java:27)

CombatDomainParticipantsTest > nonAirCombatUnitPreventsNonFightingGroundCapture() FAILED
    java.lang.NullPointerException: Cannot invoke "games.strategy.engine.data.GameData.getRelationshipTracker()" because the return value of "games.strategy.engine.data.GamePlayer.getData()" is null
        at games.strategy.engine.data.GamePlayer.isAtWar(GamePlayer.java:247)
        at games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest.setUp(CombatDomainParticipantsTest.java:27)

CombatDomainParticipantsTest > separatedRuleSplitsAirAndGroundAttackers() FAILED
    java.lang.NullPointerException: Cannot invoke "games.strategy.engine.data.GameData.getRelationshipTracker()" because the return value of "games.strategy.engine.data.GamePlayer.getData()" is null
        at games.strategy.engine.data.GamePlayer.isAtWar(GamePlayer.java:247)
        at games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest.setUp(CombatDomainParticipantsTest.java:27)

2530 tests completed, 5 failed

> Task :game-core:test FAILED
Failed tests for game-core:
games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest::infrastructureAloneDoesNotCreateGroundCombat()
games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest::legacyRuleKeepsAircraftInTheNormalBattle()
games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest::nonAirCombatUnitPreventsNonFightingGroundCapture()
games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest::separatedRuleRemovesEnemyAircraftFromGroundDefense()
games.strategy.triplea.delegate.battle.CombatDomainParticipantsTest::separatedRuleSplitsAirAndGroundAttackers()

gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/validation-1784008390468.json

[Incubating] Problems report is available at: file:///home/runner/work/triplea-rebased/triplea-rebased/build/reports/problems/problems-report.html

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':game-core:test'.
> There were failing tests. See the report at: file:///home/runner/work/triplea-rebased/triplea-rebased/game-app/game-core/build/reports/tests/test/index.html

* Try:
> Run with --scan to get full insights from a Build Scan (powered by Develocity).

* Exception is:
org.gradle.api.tasks.TaskExecutionException: Execution failed for task ':game-core:test'.
	at org.gradle.api.internal.tasks.execution.ExecuteActionsTaskExecuter.lambda$executeIfValid$1(ExecuteActionsTaskExecuter.java:135)
	at org.gradle.internal.Try$Failure.ifSuccessfulOrElse(Try.java:288)
	at org.gradle.api.internal.tasks.execution.ExecuteActionsTaskExecuter.executeIfValid(ExecuteActionsTaskExecuter.java:133)
	at org.gradle.api.internal.tasks.execution.ExecuteActionsTaskExecuter.execute(ExecuteActionsTaskExecuter.java:121)
	at org.gradle.api.internal.tasks.execution.ProblemsTaskPathTrackingTaskExecuter.execute(ProblemsTaskPathTrackingTaskExecuter.java:41)
	at org.gradle.api.internal.tasks.execution.ResolveTaskExecutionModeExecuter.execute(ResolveTaskExecutionModeExecuter.java:51)
	at org.gradle.api.internal.tasks.execution.FinalizePropertiesTaskExecuter.execute(FinalizePropertiesTaskExecuter.java:46)
	at org.gradle.api.internal.tasks.execution.SkipTaskWithNoActionsExecuter.execute(SkipTaskWithNoActionsExecuter.java:57)
	at org.gradle.api.internal.tasks.execution.SkipOnlyIfTaskExecuter.execute(SkipOnlyIfTaskExecuter.java:74)
	at org.gradle.api.internal.tasks.execution.CatchExceptionTaskExecuter.execute(CatchExceptionTaskExecuter.java:36)
	at org.gradle.api.internal.tasks.execution.EventFiringTaskExecuter$1.executeTask(EventFiringTaskExecuter.java:77)
	at org.gradle.api.internal.tasks.execution.EventFiringTaskExecuter$1.call(EventFiringTaskExecuter.java:55)
	at org.gradle.api.internal.tasks.execution.EventFiringTaskExecuter$1.call(EventFiringTaskExecuter.java:52)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$CallableBuildOperationWorker.execute(DefaultBuildOperationRunner.java:210)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$CallableBuildOperationWorker.execute(DefaultBuildOperationRunner.java:205)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:67)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:167)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.call(DefaultBuildOperationRunner.java:54)
	at org.gradle.api.internal.tasks.execution.EventFiringTaskExecuter.execute(EventFiringTaskExecuter.java:52)
	at org.gradle.execution.plan.DefaultNodeExecutor.executeLocalTaskNode(DefaultNodeExecutor.java:55)
	at org.gradle.execution.plan.DefaultNodeExecutor.execute(DefaultNodeExecutor.java:34)
	at org.gradle.execution.taskgraph.DefaultTaskExecutionGraph$InvokeNodeExecutorsAction.execute(DefaultTaskExecutionGraph.java:355)
	at org.gradle.execution.taskgraph.DefaultTaskExecutionGraph$InvokeNodeExecutorsAction.execute(DefaultTaskExecutionGraph.java:343)
	at org.gradle.execution.taskgraph.DefaultTaskExecutionGraph$BuildOperationAwareExecutionAction.lambda$execute$0(DefaultTaskExecutionGraph.java:339)
	at org.gradle.internal.operations.CurrentBuildOperationRef.with(CurrentBuildOperationRef.java:84)
	at org.gradle.execution.taskgraph.DefaultTaskExecutionGraph$BuildOperationAwareExecutionAction.execute(DefaultTaskExecutionGraph.java:339)
	at org.gradle.execution.taskgraph.DefaultTaskExecutionGraph$BuildOperationAwareExecutionAction.execute(DefaultTaskExecutionGraph.java:328)
	at org.gradle.execution.plan.DefaultPlanExecutor$ExecutorWorker.execute(DefaultPlanExecutor.java:459)
	at org.gradle.execution.plan.DefaultPlanExecutor$ExecutorWorker.run(DefaultPlanExecutor.java:376)
	at org.gradle.internal.concurrent.ExecutorPolicy$CatchAndRecordFailures.onExecute(ExecutorPolicy.java:64)
	at org.gradle.internal.concurrent.AbstractManagedExecutor$1.run(AbstractManagedExecutor.java:47)
Caused by: org.gradle.api.internal.exceptions.MarkedVerificationException: There were failing tests. See the report at: file:///home/runner/work/triplea-rebased/triplea-rebased/game-app/game-core/build/reports/tests/test/index.html
	at org.gradle.api.tasks.testing.AbstractTestTask.executeTests(AbstractTestTask.java:615)
	at org.gradle.api.tasks.testing.Test.executeTests(Test.java:760)
	at org.gradle.internal.reflect.JavaMethod.invoke(JavaMethod.java:125)
	at org.gradle.api.internal.project.taskfactory.StandardTaskAction.doExecute(StandardTaskAction.java:58)
	at org.gradle.api.internal.project.taskfactory.StandardTaskAction.execute(StandardTaskAction.java:51)
	at org.gradle.api.internal.project.taskfactory.StandardTaskAction.execute(StandardTaskAction.java:29)
	at org.gradle.api.internal.tasks.execution.TaskExecution$3.run(TaskExecution.java:259)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$1.execute(DefaultBuildOperationRunner.java:30)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$1.execute(DefaultBuildOperationRunner.java:27)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:67)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:167)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.run(DefaultBuildOperationRunner.java:48)
	at org.gradle.api.internal.tasks.execution.TaskExecution.executeAction(TaskExecution.java:244)
	at org.gradle.api.internal.tasks.execution.TaskExecution.executeActions(TaskExecution.java:227)
	at org.gradle.api.internal.tasks.execution.TaskExecution.executeWithPreviousOutputFiles(TaskExecution.java:210)
	at org.gradle.api.internal.tasks.execution.TaskExecution.execute(TaskExecution.java:176)
	at org.gradle.internal.execution.steps.ExecuteStep.executeInternal(ExecuteStep.java:167)
	at org.gradle.internal.execution.steps.ExecuteStep.access$000(ExecuteStep.java:47)
	at org.gradle.internal.execution.steps.ExecuteStep$1.call(ExecuteStep.java:137)
	at org.gradle.internal.execution.steps.ExecuteStep$1.call(ExecuteStep.java:134)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$CallableBuildOperationWorker.execute(DefaultBuildOperationRunner.java:210)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$CallableBuildOperationWorker.execute(DefaultBuildOperationRunner.java:205)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:67)
	at org.gradle.internal.operations.DefaultBuildOperationRunner$2.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:167)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.execute(DefaultBuildOperationRunner.java:60)
	at org.gradle.internal.operations.DefaultBuildOperationRunner.call(DefaultBuildOperationRunner.java:54)
	at org.gradle.internal.execution.steps.ExecuteStep.execute(ExecuteStep.java:134)
	at org.gradle.internal.execution.steps.ExecuteStep$Mutable.execute(ExecuteStep.java:80)
	at org.gradle.internal.execution.steps.CancelExecutionStep.execute(CancelExecutionStep.java:42)
	at org.gradle.internal.execution.steps.TimeoutStep.executeWithoutTimeout(TimeoutStep.java:75)
	at org.gradle.internal.execution.steps.TimeoutStep.execute(TimeoutStep.java:55)
	at org.gradle.internal.execution.steps.PreCreateOutputParentsStep.execute(PreCreateOutputParentsStep.java:51)
	at org.gradle.internal.execution.steps.PreCreateOutputParentsStep.execute(PreCreateOutputParentsStep.java:29)
	at org.gradle.internal.execution.steps.RemovePreviousOutputsStep.executeMutable(RemovePreviousOutputsStep.java:67)
	at org.gradle.internal.execution.steps.RemovePreviousOutputsStep.executeMutable(RemovePreviousOutputsStep.java:39)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.BroadcastChangingOutputsStep.execute(BroadcastChangingOutputsStep.java:42)
	at org.gradle.internal.execution.steps.BroadcastChangingOutputsStep.execute(BroadcastChangingOutputsStep.java:24)
	at org.gradle.internal.execution.steps.CaptureOutputsAfterExecutionStep.execute(CaptureOutputsAfterExecutionStep.java:69)
	at org.gradle.internal.execution.steps.CaptureOutputsAfterExecutionStep.execute(CaptureOutputsAfterExecutionStep.java:46)
	at org.gradle.internal.execution.steps.ResolveInputChangesStep.executeMutable(ResolveInputChangesStep.java:39)
	at org.gradle.internal.execution.steps.ResolveInputChangesStep.executeMutable(ResolveInputChangesStep.java:28)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.BuildCacheStep.executeWithoutCache(BuildCacheStep.java:189)
	at org.gradle.internal.execution.steps.BuildCacheStep.executeAndStoreInCache(BuildCacheStep.java:145)
	at org.gradle.internal.execution.steps.BuildCacheStep.lambda$executeWithCache$4(BuildCacheStep.java:104)
	at org.gradle.internal.execution.steps.BuildCacheStep.lambda$executeWithCache$5(BuildCacheStep.java:104)
	at org.gradle.internal.Try$Success.map(Try.java:170)
	at org.gradle.internal.execution.steps.BuildCacheStep.executeWithCache(BuildCacheStep.java:88)
	at org.gradle.internal.execution.steps.BuildCacheStep.lambda$execute$0(BuildCacheStep.java:75)
	at org.gradle.internal.Either$Left.fold(Either.java:116)
	at org.gradle.internal.execution.caching.CachingState.fold(CachingState.java:62)
	at org.gradle.internal.execution.steps.BuildCacheStep.execute(BuildCacheStep.java:74)
	at org.gradle.internal.execution.steps.BuildCacheStep.execute(BuildCacheStep.java:49)
	at org.gradle.internal.execution.steps.StoreExecutionStateStep.executeMutable(StoreExecutionStateStep.java:46)
	at org.gradle.internal.execution.steps.StoreExecutionStateStep.executeMutable(StoreExecutionStateStep.java:35)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.SkipUpToDateStep.executeBecause(SkipUpToDateStep.java:75)
	at org.gradle.internal.execution.steps.SkipUpToDateStep.lambda$execute$2(SkipUpToDateStep.java:53)
	at org.gradle.internal.execution.steps.SkipUpToDateStep.execute(SkipUpToDateStep.java:53)
	at org.gradle.internal.execution.steps.SkipUpToDateStep.execute(SkipUpToDateStep.java:35)
	at org.gradle.internal.execution.steps.legacy.MarkSnapshottingInputsFinishedStep.execute(MarkSnapshottingInputsFinishedStep.java:37)
	at org.gradle.internal.execution.steps.legacy.MarkSnapshottingInputsFinishedStep.execute(MarkSnapshottingInputsFinishedStep.java:27)
	at org.gradle.internal.execution.steps.ResolveMutableCachingStateStep.executeDelegate(ResolveMutableCachingStateStep.java:70)
	at org.gradle.internal.execution.steps.ResolveMutableCachingStateStep.executeDelegate(ResolveMutableCachingStateStep.java:32)
	at org.gradle.internal.execution.steps.AbstractResolveCachingStateStep.execute(AbstractResolveCachingStateStep.java:69)
	at org.gradle.internal.execution.steps.AbstractResolveCachingStateStep.execute(AbstractResolveCachingStateStep.java:37)
	at org.gradle.internal.execution.steps.ResolveChangesStep.executeMutable(ResolveChangesStep.java:63)
	at org.gradle.internal.execution.steps.ResolveChangesStep.executeMutable(ResolveChangesStep.java:34)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.ValidateStep$Mutable.executeDelegate(ValidateStep.java:79)
	at org.gradle.internal.execution.steps.ValidateStep$Mutable.executeDelegate(ValidateStep.java:65)
	at org.gradle.internal.execution.steps.ValidateStep.execute(ValidateStep.java:105)
	at org.gradle.internal.execution.steps.ValidateStep$Mutable.execute(ValidateStep.java:65)
	at org.gradle.internal.execution.steps.CaptureMutableStateBeforeExecutionStep.executeMutable(CaptureMutableStateBeforeExecutionStep.java:86)
	at org.gradle.internal.execution.steps.CaptureMutableStateBeforeExecutionStep.execute(CaptureMutableStateBeforeExecutionStep.java:65)
	at org.gradle.internal.execution.steps.CaptureMutableStateBeforeExecutionStep.execute(CaptureMutableStateBeforeExecutionStep.java:45)
	at org.gradle.internal.execution.steps.SkipEmptyMutableWorkStep.executeWithNonEmptySources(SkipEmptyMutableWorkStep.java:210)
	at org.gradle.internal.execution.steps.SkipEmptyMutableWorkStep.executeMutable(SkipEmptyMutableWorkStep.java:90)
	at org.gradle.internal.execution.steps.SkipEmptyMutableWorkStep.executeMutable(SkipEmptyMutableWorkStep.java:53)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.legacy.MarkSnapshottingInputsStartedStep.execute(MarkSnapshottingInputsStartedStep.java:38)
	at org.gradle.internal.execution.steps.LoadPreviousExecutionStateStep.executeMutable(LoadPreviousExecutionStateStep.java:36)
	at org.gradle.internal.execution.steps.LoadPreviousExecutionStateStep.executeMutable(LoadPreviousExecutionStateStep.java:23)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.HandleStaleOutputsStep.executeMutable(HandleStaleOutputsStep.java:77)
	at org.gradle.internal.execution.steps.HandleStaleOutputsStep.executeMutable(HandleStaleOutputsStep.java:43)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.AssignMutableWorkspaceStep.lambda$executeMutable$0(AssignMutableWorkspaceStep.java:34)
	at org.gradle.api.internal.tasks.execution.TaskExecution$4.withWorkspace(TaskExecution.java:305)
	at org.gradle.internal.execution.steps.AssignMutableWorkspaceStep.executeMutable(AssignMutableWorkspaceStep.java:30)
	at org.gradle.internal.execution.steps.AssignMutableWorkspaceStep.executeMutable(AssignMutableWorkspaceStep.java:21)
	at org.gradle.internal.execution.steps.MutableStep.execute(MutableStep.java:26)
	at org.gradle.internal.execution.steps.ChoosePipelineStep.execute(ChoosePipelineStep.java:40)
	at org.gradle.internal.execution.steps.ChoosePipelineStep.execute(ChoosePipelineStep.java:23)
	at org.gradle.internal.execution.steps.ExecuteWorkBuildOperationFiringStep.lambda$execute$2(ExecuteWorkBuildOperationFiringStep.java:67)
	at org.gradle.internal.execution.steps.ExecuteWorkBuildOperationFiringStep.execute(ExecuteWorkBuildOperationFiringStep.java:67)
	at org.gradle.internal.execution.steps.ExecuteWorkBuildOperationFiringStep.execute(ExecuteWorkBuildOperationFiringStep.java:39)
	at org.gradle.internal.execution.steps.IdentityCacheStep.execute(IdentityCacheStep.java:46)
	at org.gradle.internal.execution.steps.IdentityCacheStep.execute(IdentityCacheStep.java:34)
	at org.gradle.internal.execution.steps.IdentifyStep.execute(IdentifyStep.java:56)
	at org.gradle.internal.execution.steps.IdentifyStep.execute(IdentifyStep.java:38)
	at org.gradle.internal.execution.impl.DefaultExecutionEngine$1.execute(DefaultExecutionEngine.java:68)
	at org.gradle.api.internal.tasks.execution.ExecuteActionsTaskExecuter.executeIfValid(ExecuteActionsTaskExecuter.java:132)
	... 30 more


BUILD FAILED in 4m 15s
154 actionable tasks: 152 executed, 2 from cache
Configuration cache entry stored.
```
