# Nose

## Getting started

First, follow the steps in the [Getting started](../getting-started.md) guide to install the Launchable CLI, set your API key, and verify your connection.

Then return to this page to complete the integration.

## Recording a build

Launchable chooses which tests to run based on the changes contained in a **build**. To enable this, you need to send build information to Launchable.

Right before you create a build in your CI script, invoke the Launchable CLI as follows:

```bash
launchable record build --name <BUILD NAME> --source src=<PATH TO SOURCE>
```

With the `--name` option, you assign a unique identifier to this build. You will use this value later when you request a subset and record test results. See [Choosing a value for `<BUILD NAME>`](../resources/build-names.md) for tips on choosing this value.

The `--source` option points to the local copy of the Git repository used to produce this build, such as `.` or `src`.

## Subsetting tests

First, install the Launchable plugin for Nose using PIP:

```bash
$ pip install nose-launchable
```

To run a meaningful subset of tests, invoke `nosetests` with three extra flags:

```bash
# subset tests with Launchable
nosetests --launchable-build-number <BUILD NAME> \
  --launchable-subset \
  --launchable-subset-options <LAUNCHABLE CLI SUBSET OPTIONS>
```

The `--launchable-build-number` flag tells Launchable which build is being tested. This should be the same value you used for `--name` in `launchable record build` before. The `--launchable-subset` flag enables subsetting. 

The `--launchable-subset-options` flag tells the plugin which Launchable CLI subset options to use. For example, to use the Launchable CLI's `--target` option, the flag should look like `--launchable-subset-options '--target 10%'`. This runs a subset of the most useful test targets that will run in 10% of the full execution time. You can also use `--launchable-subset-options '--time 100'` to run a subset of the most useful test targets that will run in 100 seconds. See the [CLI reference](../resources/cli-reference.md) for more options.

{% hint style="info" %}
The `--launchable-subset-target PERCENTAGE` option is still available; it functions the same as `--launchable-subset-options '--target PERCENTAGE'`. To accommodate future CLI options, however, we recommend using `--launchable-subset-options` where convenient.
{% endhint %}

## Recording test results

The Nose plugin automatically sends test results to Launchable when you run Nose with `--launchable-subset` enabled.

However, if you want to submit test reports from a full test run to help train the model, run your tests with the `--launchable-record-only` flag:

```bash
nosetests --launchable-build-number <BUILD NAME> \
  --launchable-record-only
```

## Troubleshooting

If you encounter issues running Nose with the Launchable plugin, you can set the `LAUNCHABLE_DEBUG` environment variable to `1` before running tests to print debug logs.

```bash
# enable debug logs
export LAUNCHABLE_DEBUG=1

# run tests with Launchable
nosetests --launchable-subset ...
```

## Development

The Launchable Nose plugin is open source and [available on GitHub](https://github.com/launchableinc/nose-launchable). Pull requests are always appreciated!

