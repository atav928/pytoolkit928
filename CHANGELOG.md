# Releases

## v0.0.12

* Fixed issue with regex that doesn't match correctly.

## v0.0.11

* __BUG:__ issue with typing on retry decorator.
* Updated failed pytest coverage to install test modules.

## v0.0.10

* Added SplunkHec dataclass.
* Added Nested Dataclass decorator.
* Added additional UnitTests.
* Updated deploy and codeql pipelines.

## v0.0.9

* Cleaned up Base Dataclass module.
* Added additional file checks.
* Added code checks.
* Aded Snyk validation for vulnerabilities.
* Added pipelines for auto testing.
* Added dataclass nested structure.

## v0.0.8

* __HOTFIX:__ issue with set dir.

## v0.0.7

* Added file manipulations.

## v0.0.6

* Added Base Monitor for dataclass that includes some common methods.
* Added Unit test and set pass to 50%.

## v0.0.5

* Added nest dict function.
* Added Unit testing.
* Updated Readme.

## v0.0.4

* Added Flatten Dictionary function.
* Added Hostname and FQDN System Hostname return.
* Added grabbing current username.

## v0.0.3

* Added delimeter option.
  * Allows you to specify the delimeter you want to use using an OR operation with `|`.
* __WARNING:__ this changes the default behavior to the original intent of turning a string to a string without using the default split(',').
