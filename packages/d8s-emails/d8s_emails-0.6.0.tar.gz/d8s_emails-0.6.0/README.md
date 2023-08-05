# Democritus Emails

[![PyPI](https://img.shields.io/pypi/v/d8s-emails.svg)](https://pypi.python.org/pypi/d8s-emails)
[![CI](https://github.com/democritus-project/d8s-emails/workflows/CI/badge.svg)](https://github.com/democritus-project/d8s-emails/actions)
[![Lint](https://github.com/democritus-project/d8s-emails/workflows/Lint/badge.svg)](https://github.com/democritus-project/d8s-emails/actions)
[![codecov](https://codecov.io/gh/democritus-project/d8s-emails/branch/main/graph/badge.svg?token=V0WOIXRGMM)](https://codecov.io/gh/democritus-project/d8s-emails)
[![The Democritus Project uses semver version 2.0.0](https://img.shields.io/badge/-semver%20v2.0.0-22bfda)](https://semver.org/spec/v2.0.0.html)
[![The Democritus Project uses black to format code](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://choosealicense.com/licenses/lgpl-3.0/)

Democritus functions<sup>[1]</sup> for working with emails.

[1] Democritus functions are <i>simple, effective, modular, well-tested, and well-documented</i> Python functions.

We use `d8s` (pronounced "dee-eights") as an abbreviation for `democritus` (you can read more about this [here](https://github.com/democritus-project/roadmap#what-is-d8s)).

## Installation

```
pip install d8s-emails
```

## Usage

You import the library like:

```python
from d8s_emails import *
```

Once imported, you can use any of the functions listed below.

## Functions

  - ```python
    def is_email(possible_email_text: str) -> bool:
        """Determine if the given string is an email."""
    ```
  - ```python
    def email_header_date_fix(email_text: str):
        """Fix the `Date` header in the given email email_text."""
    ```
  - ```python
    def email_read(email_string: str):
        """."""
    ```
  - ```python
    def email_object_new():
        """."""
    ```
  - ```python
    def email_content_transfer_encoding(email_text):
        """Get the content-transfer-encoding for the email (see https://www.w3.org/Protocols/rfc1341/5_Content-Transfer-Encoding.html)."""
    ```
  - ```python
    def email_bodies_as_strings(email_text):
        """Return the bodies (as strings) for the given email."""
    ```
  - ```python
    def email_bodies_as_objects(email_text):
        """Return the bodies (as objects) for the given email."""
    ```
  - ```python
    def email_attachments(email_text):
        """Return the attachments (as strings) for the given email."""
    ```
  - ```python
    def email_attachments_objects(email_text):
        """Return the attachments (as objects) for the given email."""
    ```
  - ```python
    def email_body_is_base64(email_text):
        """Determine if the body of the email is encoded using base64."""
    ```
  - ```python
    def email_header_fields(email_text):
        """Get the header fields in the email."""
    ```
  - ```python
    def email_headers(email_text):
        """Get the values of the header fields in the email."""
    ```
  - ```python
    def email_headers_raw(email_text):
        """Get the raw (undecoded) values of the header fields in the email."""
    ```
  - ```python
    def email_headers_as_dict(email_text) -> Dict[str, List[str]]:
        """Return email's header fields as a dictionary with the header field key as the dictionary's key and the header field value as the dictionary's value."""
    ```
  - ```python
    def email_header(email_text, header_field):
        """Get the value(s) for the given header fields."""
    ```
  - ```python
    def email_header_delete_field(email_text, header_field):
        """Delete the header_field from the email_text."""
    ```
  - ```python
    def email_structure(email_text):
        """Get the structure of the email (this function was inspired by the function here: https://github.com/python/cpython/blob/4993cc0a5b34dc91da2b41c50e33d809f0191355/Lib/email/iterators.py#L59 - which is described here: https://docs.python.org/3.5/library/email.iterators.html?highlight=_structure#email.iterators._structure)."""
    ```
  - ```python
    def email_header_add_raw(email, header_name, header_value):
        """Add a header to the email."""
    ```
  - ```python
    def email_header_add(email, header_name, header_value):
        """Add a header to the email."""
    ```

## Development

👋 &nbsp;If you want to get involved in this project, we have some short, helpful guides below:

- [contribute to this project 🥇][contributing]
- [test it 🧪][local-dev]
- [lint it 🧹][local-dev]
- [explore it 🔭][local-dev]

If you have any questions or there is anything we did not cover, please raise an issue and we'll be happy to help.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and Floyd Hightower's [Python project template](https://github.com/fhightower-templates/python-project-template).

[contributing]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#contributing-a-pr-
[local-dev]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#local-development-
