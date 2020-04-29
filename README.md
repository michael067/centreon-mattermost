Centreon Mattermost Plugin
========================

A plugin for [Centreon](https://www.centreon.com/) to enable notifications to a [Mattermost](http://www.mattermost.org/) server.

## Plugin Usage

Run `./mattermost.py --help` for full usage information.

## Required for centos

yum install python3

pip3 install requests

pip3 install argparse

## Mattermost Configuration

1. *Incoming Webhooks* must be enabled for your Mattermost server. Check the **Enable Incoming Webhooks** option under **Service Settings** in the *System Console*.

2. To use the optional `--username` parameter you must enable overriding of usernames from webhooks. Check the **Enable Overriding Usernames from Webhooks and Slash Commands** option under **Service Settings** in the *System Console*.

3. To use the optional `--iconurl` parameter you must enable overriding of icons from webhooks. Check the **Enable Overriding Icon from Webhooks and Slash Commands** option under **Service Settings** in the *System Console*.

## Centreon Configuration

The steps below are for a Centreon 20.04 server but should work with minimal modifications for compatible software:

1. Copy `mattermost.py` to `/usr/lib/centreon/plugins`.

    wget -O /usr/lib/centreon/plugins/mattermost.py https://raw.githubusercontent.com/michael067/centreon-mattermost/master/mattermost.py
    
    chmod +x /usr/lib/centreon/plugins/mattermost.py
    
2. Create an *Incoming Webhook* integration for the approriate team and note the provided URL.

3. Create the command definitions in your Centreon configuration: 

   Configuration - Commands - Notifications
   
   Add
   
   host-notify-by-mattermost
    ```
    $CENTREONPLUGINS$/mattermost.py --url "$CONTACTEMAIL$" \
    --channel "$CONTACTPAGER$" \
    --username "$CONTACTNAME$" \
    --notificationtype "$NOTIFICATIONTYPE$" \
    --hostalias "$HOSTNAME$" \
    --hostaddress "$HOSTADDRESS$" \
    --hoststate "$HOSTSTATE$" \
    --hostoutput "$HOSTOUTPUT$"
    ```
    Add
    
    service-notify-by-mattermost
    ```
    $CENTREONPLUGINS$/mattermost.py --url "$CONTACTEMAIL$" \
    --channel "$CONTACTPAGER$" \
    --username "$CONTACTNAME$" \
    --notificationtype "$NOTIFICATIONTYPE$" \
    --hostalias "$HOSTNAME$" \
    --hostaddress "$HOSTADDRESS$" \
    --servicedesc "$SERVICEDESC$" \
    --servicestate "$SERVICESTATE$" \
    --serviceoutput "$SERVICEOUTPUT$"
    ```

4. Create the contacts/Users definition in your Centreon configuration:
   Access Disabled, Status Enabled
    ```
    Login                                mattermost
    Full Name                            Centreon  ( Username in Mattermost ) 
    Email                                https://mattermost_hook... ( required )
    Pager                                Channel in mattermost ( optional )
    service_notification_period          24x7
    host_notification_period             24x7
    service_notification_options         w,u,c,r
    host_notification_options            d,u,rr
    host_notification_commands           host-notify-by-mattermost
    service_notification_commands        service-notify-by-mattermost
   ```

5. Add the contact to a contact group in your Centreon configuration:

    ```
    contactgroup_name       Supervisors
    alias                   Centreon supervisors
    members                 mattermost
    ```
