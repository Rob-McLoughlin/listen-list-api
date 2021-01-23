## Commit types
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- type: describes the category of the change. See [supported types](#commit-types).
- scope: (optional) describes what is affected by the change
- subject: a small description of the change
- body: (optional) additional contextual information about the change
- footer: (optional) adds external links, issue references and other meta-information

i.e.: 

```
chore: automate release
fix(styles): fix button padding
feat(script): add auto focus to fields with errors
```

The list bellow describes the supported commit types and their effect in the release and changelog.

| Type     | Description                                                                                            | Release | Changelog                |
|----------|--------------------------------------------------------------------------------------------------------|---------|--------------------------|
| build    | Changes that affect the build system or external dependencies                                          | -       | -                        |
| chore    | Other changes that don't modify the source code                                                        | -       | -                        |
| ci       | Changes to our CI configuration files and scripts                                                      | -       | -                        |
| docs     | Documentation only changes                                                                             | -       | -                        |
| feat     | A new feature                                                                                          | minor   | Features                 |
| fix      | A bug fix                                                                                              | patch   | Bug Fixes                |
| perf     | A code change that improves performance                                                                | patch   | Performance Improvements |
| refactor | A code change that neither fixes a bug nor adds a feature                                              | -       | -                        |
| revert   | Reverts a previous commit                                                                              | patch   | Reverts                  |
| style    | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) | -       | -                        |
| test     | Adding missing tests or correcting existing tests                                                      | -       | -                        |