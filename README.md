# JSON2HTML
A transpiler that lets you write entire websites in JSON. Built for Flask.

## Data Models

### to_replace dict
They key is the string to replace, and the value is the string to replace it with.
When not specifying a string type, the transpiler will cast the value to a string.

| key type | value  |
| -------- | ------ |
| str      | object |

## Documentation

These are the methods you'll mostly be using:
### from_json

| argument       | type   | description                                                                                                  |
| -------------- | ------ | ------------------------------------------------------------------------------------------------------------ |
| code           | object | JSON object of the page you're trying to transpile.                                                          |
| to_replace?    | array  | Array of to_replace dicts where the key is the string to replace, and the value is the value to replace with.|

#### Returns
HTML string if successful, HTML string of 404 page, which also returns a 404 status code for Flask.

### from_json_file

| argument       | type   | description                                                                                                  |
| -------------- | ------ | ------------------------------------------------------------------------------------------------------------ |
| filename       | string | Path to the JSON file you're trying to transpile.                                                            |
| to_replace?    | array  | Array of to_replace dicts where the key is the string to replace, and the value is the value to replace with.|

#### Returns
HTML string if successful, HTML string of 404 page, which also returns a 404 status code for Flask.

## Examples

```json
{
	"head": {
		"title": "KS is a cutie",
		"links": [
				{
            "rel": "stylesheet",
             "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
             "integrity": "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
             "crossorigin": "anonymous"
        }
     ]
	},
	"body": [
		{
			"type": "div",
			"arguments": [{"style": "background-color: black; color: white;"}],
			"children": [
				{
					"type": "h1",
					"content": "KS is a cutie"
				},
				{
					"type": "h3",
					"content": "He keeps denying it but he's objectively wrong."
				}
			]
		}
	]
}
```
