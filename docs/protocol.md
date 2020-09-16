# Taki - Communication Protocol

## Introduction

Our Taki game is based on regular client-server communication. This document formalizes the conventions used for communicating between the server and the different clients, by defining a formal communication protocol.

The protocol consists of JSON-based messages, due to the fact that they are very easy to parse, and also very easy to define and understand, thus, flattening the learning curve for the client-side developers. The authentication method used in the protocol is based on JWT (JSON Web Tokens), which provide a wonderful way to sign data and pass it around safely.

## Protocol Flow

The protocol defines a standard flow for the communication, which is based on the interaction with the user application. The flow is as follows:

1. The user opens the game, while creating a communication session with the server.
2. The user creates / joins a game, which in turn causes the server to generate a JWT for later authentication.
3. The game starts (as a result of the game creator's decision), and all the players are notified.
4. Each player, in its turn (which is defined by the server), gets the opportunity to do a move.
5. Three out of four players finally get rid of all of their cards, which then causes the game to end.
6. The flow gets back to step number 2. All the JWTs are not relevant anymore.

## Side Notes

1. If a player does not make a move after 30 seconds from the server's request, the server automatically relates to it as a *take_cards* request.

## Messages

1. [Creating a Game](#creating-a-game)
2. [Joining a Game](#joining-a-game)
3. [Leaving a Game](#leaving-a-game)
4. [Starting a Game](#starting-a-game)
5. [Update Turn](#update-turn)
6. [Doing a Move](#doing-a-move)
7. [Ending a Game](#ending-a-game)
8. [General Bad Request](#general-bad-request)

### Creating a Game

**Request:**

```json
{
    "code": "create_game",
    "args": {
        "lobby_name" :  "",
        "player_name" : "",
        "password":     ""
    }
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {
        "game_id":  "",
        "jwt":      ""
    }
}
```

### Joining a Game

**Request:**

```json
{
    "code": "join_game",
    "args": {
        "game_id":      "",
        "player_name":  "",
        "password" :    ""
    }
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {
        "jwt": ""
    }
}
```

**Bad Request Response:**

```json
{
    "status": "bad_request",
    "args": {
        "message": "One of the fields in the request is empty / invalid"
    }
}
```

**Conflict Response:**

```json
{
    "status": "conflict",
    "args": {
        "message": "The chosen name is already taken"
    }
}
```

**Not Found Response:**

```json
{
    "status": "not_found",
    "args": {
        "message": "A game with the supplied game ID was not found"
    }
}
```

**Denied Responses:**

```json
{
    "status": "denied",
    "args": {
        "message": "The game has already started"
    }
}
```

```json
{
    "status": "denied",
    "args": {
        "message": "The game lobby is full"
    }
}
```

**Server Broadcast Message:**

```json
{
    "code": "player_joined",
    "args": {
        "player_name": ""
    }
}
```

### Leaving a Game

**Request:**

```json
{
    "code": "leave_game",
    "jwt":  "",
    "args": {}
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {}
}
```

**Server Broadcast Message:**

```json
{
    "code": "player_left",
    "args": {
        "player_name": ""
    }
}
```

### Starting a Game

**Request:**

```json
{
    "code": "start_game",
    "jwt":  "",
    "args": {}
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {}
}
```

**Denied Responses:**

```json
{
    "status": "denied",
    "args": {
        "message": "You are alone in the lobby"
    }
}
```

```json
{
    "status": "denied",
    "args": {
        "message": "You are not the administrator of the lobby"
    }
}
```

**Server Broadcast Message:**

This message is not a real broadcast message. It is sent to each user separately, and contains player-specific data, like his cards. Furthermore, the players argument contains the player names, in a relative order to the player the message is sent to, hence, making the client-side rendering easier.

```json
{
    "code": "game_starting",
    "args": {
        "players":  [],
        "cards":    []
    }
}
```

### Update Turn

**Server Broadcast Message:**

```json
{
    "code": "update_turn",
    "args": {
        "current_player": ""
    }
}
```

### Doing a Move

**Card Placement Request:**

```json
{
    "code": "place_cards",
    "jwt":  "",
    "args": {
        "cards": []
    }
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {}
}
```

**Bad Request Response:**

```json
{
    "status": "bad_request",
    "args": {
        "message": "Invalid move done."
    }
}
```

**Server Broadcast Message:**

```json
{
    "code": "move_done",
    "args": {
        "type":         "cards_placed",
        "cards":        [],
        "player_name":  ""
    }
}
```

**Card Taking Request:**

```json
{
    "code": "take_cards",
    "jwt":  "",
    "args": {}
}
```

**Success Response:**

```json
{
    "status": "success",
    "args": {
        "cards": []
    }
}
```

**Server Broadcast Message:**

```json
{
    "code": "move_done",
    "args": {
        "type":         "cards_taken",
        "amount":       0,
        "player_name":  ""
    }
}
```

### Ending a Game

**Server Broadcast Message:**

```json
{
    "code": "player_won",
    "args": {
        "player_name": ""
    }
}
```

**Server Broadcast Message:**

```json
{
    "code": "game_ended",
    "args": {
        "scoreboard": []
    }
}
```

### General Bad Request

**Bad Request Response:**

```json
{
    "status": "bad_request",
    "args": {
        "message": "Bad request"
    }
}
```