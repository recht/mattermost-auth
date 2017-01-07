# Utility for extracting a Mattermost auth token.

This is intended to be used with the [Mattermost IRC gateway](https://github.com/42wim/matterircd) when SAML authentication has been enabled.

The plugin works by launching a Chrome browser and authenticating a session. Once authenticated, the session
cookie will be extraced and saved to `~/.mmauthtoken`. The script then output a login line for the IRC gateway.

To install:

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python setup.py develop
```

To use from Weechat to automatically authenticate at login set `irc.server.matter.command` to
`"/query -server $server mattermost; /exec -o -buffer irc.$server.mattermost PATH_TO_VIRTUALENV/bin/mattermost-auth -d <domainname> -t <teamname> -u <username>`
