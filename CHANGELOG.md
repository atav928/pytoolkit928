# Releases

## v0.0.15

* Removed SSH and Pamiko module; split over to another project.
* Add chunk/split into splunk upload.

## v0.0.14

* __BUG:__ Import error.
__Todo:__

* Add import key option to SSH Client.
  * Uae ability to pass a string ot byte feom me
ory.
  * Use add from file.
  * Block Password if using Key.
* Update to extract method to enhanxe the callable lambda fucntions.
  * Add readme to make more usable.

## v0.0.12

* Fixed issue with regex that doesn't match correctly.
* Added function to create ability to search for a configuraiton file based on passed ordered list of places to search for a configuration file to read.
* Added remote ssh connector.

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
