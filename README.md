# bkp-tool
## requirements
- discord-webhook
```
pip3 install discord-webhook
```
## about the bkp-tool
script loops through all subdirectories of source and syncs to destination folder.

## mandatory arguments
| arg | description |
| :-: | :-: |
| src | ... |
| dst | ... |

Example:
```
./bkp-tool.py /var/data/movies /backup/movies
```

## optional arguments
| arg | description |
| :-: | :-: |
| -f | ... |
| --show-logs | ... |
| --show-errors | ... |