# Bluezelle Discord Bot

Discord Bot for gathering data from the Bluzelle Network and publishing it into a discord server.

**Currently only supports the private testnet**, can be easily configured to support other networks once they hit Stargate.

## Usage

Supports Discord's new [slash commands](https://discord.com/developers/docs/interactions/slash-commands), which makes using the bot much easier for the user.

Every command and their description can be accessed by typing `/`:

![usage_gif](https://user-images.githubusercontent.com/36865381/126083465-1aecb708-a7c9-4a0c-a185-6b4a27293277.gif)

## Commands

- **User Commands**
  - **<a href="#Balance">/balance </a>**
  - **<a href="#Block">/block </a>**
  - **<a href="#CommunityPool">/community_pool </a>**
  - **<a href="#Inflation">/inflation </a>**
  - **<a href="#Price">/price </a>**
  - **<a href="#ProposalGetDetails">/proposal get details </a>**
  - **<a href="#ProposalGetAll">/proposal get all </a>**
  - **<a href="#Transaction">/transaction </a>**
  - **<a href="#ValidatorGetDelegations">/validator get delegations </a>**
  - **<a href="#ValidatorGetDetails">/validator get details </a>**
  - **<a href="#ValidatorGetAll">/validator get all </a>**
- **Admin Commands**
  - **<a href="#TaskGetAll">/task get all </a>**
  - **<a href="#TaskAdd">/task add </a>**
  - **<a href="#TaskDelete">/task delete </a>**

## User Commands

    <param> => Required Parameter
    [param] => Optional Parameter

- ### /balance \<address\> <a id="Balance"></a>

Get balance of an account.

![balance_output](https://user-images.githubusercontent.com/36865381/126080007-67f1fef6-c5f0-41f3-bc51-4c5e3545f546.png)

| Parameter   | Description     |
| :---------- | :-------------- |
| \<address\> | Account address |

- ### /block [height] <a id="Block"></a>

Get a block at a certain heigh.

![block_output](https://user-images.githubusercontent.com/36865381/126080218-eca93c68-3c9f-45c6-ac12-58cfa7e2dfbf.png)

| Parameter | Description                                |
| :-------- | :----------------------------------------- |
| [height]  | Height of the block. Defaults to "latest". |

- ### /community_pool <a id="CommunityPool"></a>

Get community pool coins.

![community_pool_output](https://user-images.githubusercontent.com/36865381/126080204-75b55a4d-0ad8-4e8d-be0f-b6f497a9f229.png)

- ### /inflation <a id="Inflation"></a>

Get current minting inflation value.

![inflation_output](https://user-images.githubusercontent.com/36865381/126080276-98713544-e152-4e51-9403-3e1619f24f1f.png)

- ### /price [coin] <a id="Price"></a>

Get the price of a crypto coin.

![price_output](https://user-images.githubusercontent.com/36865381/126080303-b81bdf9c-9927-44a2-b5b1-81ad74b06c8a.png)

| Parameter | Description                            |
| :-------- | :------------------------------------- |
| [coin]    | Symbol of the coin. Defaults to "BLZ". |

- ### /proposal get details \<id\> <a id="ProposalGetDetails"></a>

![proposal_get_details](https://user-images.githubusercontent.com/36865381/126179845-f8fdc1ec-462a-43c7-a2c8-b075e6d790d4.png)

| Parameter | Description         |
| :-------- | :------------------ |
| \<id\>    | Id of the proposal. |

- ### /proposal get all <a id="ProposalGetAll"></a>

Get the list of all proposals.

![proposal_get_all](https://user-images.githubusercontent.com/36865381/126164081-0b5b5c6f-2e7e-461e-a1fe-989bc7fdd2eb.png)

- ### /transaction \<hash\> <a id="Transaction"></a>

Get transaction details.

![transaction_output](https://user-images.githubusercontent.com/36865381/126080372-6f60a595-eb59-42d1-9110-7051b75fd34d.png)

| Parameter | Description                |
| :-------- | :------------------------- |
| \<hash\>  | # Hash of the transaction. |

- ### /validator get delegations \<address\> <a id="ValidatorGetDelegations"></a>

Get delegations of given validator.

![validation_get_delegations_output](https://user-images.githubusercontent.com/36865381/126080471-6d04600e-76fd-4781-9eed-24ab0a558059.png)

| Parameter   | Description       |
| :---------- | :---------------- |
| \<address\> | Validator address |

- ### /validator get details \<address\> <a id="ValidatorGetDetails"></a>

Get details of given validator.

![validator_get_details_output](https://user-images.githubusercontent.com/36865381/126080468-d57cb0e5-25eb-4167-878c-0ba303cd2eaa.png)

| Parameter   | Description       |
| :---------- | :---------------- |
| \<address\> | Validator address |

- ### /validator get all <a id="ValidatorGetAll"></a>

Get the list of all validators.

![validator_get_all_output](https://user-images.githubusercontent.com/36865381/126080466-9310725f-bf21-4cc7-94ea-e13323df4026.png)

## Admin Commands

    <param> => Required Parameter
    [param] => Optional Parameter

- ### /task get all <a id="TaskGetAll"></a>

Get the list of all active tasks.

- ### /task add \<channel\> \<interval\> \<function\> [parameters] <a id="TaskAdd"></a>

Add a task which will repeat given function per interval.

![adding_task_gif](https://user-images.githubusercontent.com/36865381/126083674-cc5f742e-efcf-4410-b298-f99222a89a8c.gif)

| Parameter    | Description                            |
| :----------- | :------------------------------------- |
| \<channel\>  | Link to the channel \*                 |
| \<interval\> | Repeat interval of the task in seconds |
| \<function\> | Name of the function \*\*              |
| [parameters] | Parameters of the function \*\*\*      |

\*Note: Channel links must have '#' at the start. (E.g. #general)

\*\*Note: Function names must be without '/' and must include '\_' instead of spaces. (E.g. validator_get_details)

\*\*\*Note: Parameters must be listed back to back seperated by spaces. (E.g. param1 param2 param3)

Note: If the added task uses paginated responses, calls response might stay in 'Bluzelle Bot is thinking...' state until the timeout of the first function is reached, in order to confirm that it was executed successfully. Response will update once the timeout is reached.

- ### /task delete \<id\> <a id="TaskDelete"></a>

Delete a task by id.

| Parameter | Description    |
| :-------- | :------------- |
| \<id\>    | Id of the task |

## Development

To use this discord bot, you must have a bot set up through the discord developers portal.

Then simply install the requirements and run `py -3 bot/main.py --secret_token <your_token>`

### More specifically:

#### Set up the bot:

- Log in to [discord.com/developers/applications](https://discord.com/developers/applications).

- Create a new application.

![new_application](https://user-images.githubusercontent.com/36865381/126081370-98dba024-42ac-466b-a93d-b668289098cc.png)

- Give the application a name and click `Create`.

![name_create](https://user-images.githubusercontent.com/36865381/126083099-d048cf8c-a7e7-4234-a49d-b64fb782d7b9.png)

- Navigate to `Bot` and click `Add Bot`.

![build_a_bot](https://user-images.githubusercontent.com/36865381/126081658-3917ef70-1815-45f6-96ba-fb505a5d94b2.png)

- Copy your secret token and save it, you will use it to start the bot later.

![copy_token](https://user-images.githubusercontent.com/36865381/126081629-4d6d109b-a4bc-4f4f-b97f-8bd084be798c.png)

- Scroll down and enable following options:

![privileged_intents](https://user-images.githubusercontent.com/36865381/126081172-1b02516b-c1ab-4301-a711-00625a9645f0.png)

- Navigate to `OAuth2`, scroll down and check the following boxes:

![scopes_permissions](https://user-images.githubusercontent.com/36865381/126082212-6e58c308-6c7e-4fdd-863f-0700ccf4a64c.png)

**<a href="#Important">IMPORTANT: Run the bot first before inviting to bot into your server. </a>**

- Open the link you just generated and click `Continue`.

![add_the_bot](https://user-images.githubusercontent.com/36865381/126081850-97fe1f74-7f11-4471-8ae5-2d01389bdc2c.png)

- Ensure the bot has the right permissions and click `Authorize`.

![authorize](https://user-images.githubusercontent.com/36865381/126081922-00789aa2-1c61-48b1-9190-da7ab826ea9e.png)

- If you see something like the image below, you've successfully added the bot into your server!

![authorized](https://user-images.githubusercontent.com/36865381/126081990-f8e2f87e-c22b-414f-8c08-248220aff306.png)

#### Run the code:

- `python -m venv venv`

- Linux/MacOS: `source venv/bin/activate`, Windows: `.\venv\Scripts\Activate.ps1`

- `pip install -r requirements.txt`

- `python configs/write_config.py`

- Enter your secret token into 'configs/config.ini'

- `python bot/main.py`

#### Important <a id="Important"></a>

In order to see the slash commands, the commands first must be uploaded to the discord's slash commands API.
To ensure that, run the bot at least once before adding it to the server.

If you can't see the slash commands below after typing `/`, kick and reinvite the bot after running it.

![slash_commands](https://user-images.githubusercontent.com/36865381/126082805-c7661f6e-5337-4116-b50d-131a1fdf293a.png)
