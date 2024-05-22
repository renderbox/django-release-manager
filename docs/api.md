### Markdown Documentation for the Release Management API

---

## Release Management API

The Release Management API allows for the creation of new software releases and the updating of release file paths. Below are the details for using the API endpoints.

### Authentication

All API requests require authentication. Clients must provide a valid token in the `Authorization` header of each request.

#### Example

```plaintext
Authorization: Token your_token_here
```

---

### Create a New Release

This endpoint is used to create a new release of a software package.

- **URL**

  `/api/releases/new/`

- **Method:**

  `POST`

- **Data Params**

  Required:

  ```json
  {
    "package": "[string] - The package identifier",
    "version": "[string] - The release version",
    "release_date": "[datetime] - The release date and time in ISO 8601 format",
    "status": "[integer] - The status code of the release (e.g., 30 for Released)",
    "release_notes": "[string] - Optional. Notes describing the release",
    "files": "[json] - Optional. JSON object representing file paths",
    "signature": "[string] - Optional. A digital signature for release integrity"
  }
  ```

- **Success Response:**

  - **Code:** 201 CREATED
  - **Content:**

    ```json
    {
      "id": 12,
      "package": "test_package",
      "version": "1.1",
      "release_date": "2024-05-22T12:00:00Z",
      "status": 30,
      "release_notes": "Added new features."
    }
    ```

- **Error Response:**

  - **Code:** 401 UNAUTHORIZED
  - **Content:** `{ error : "Authentication credentials were not provided." }`

---

### Update Release Files

This endpoint updates the file paths stored in the `files` JSON field of an existing release.

- **URL**

  `/api/releases/<int:id>/update_files/`

- **Method:**

  `PATCH`

- **URL Params**

  **Required:**

  `id=[integer]`

- **Data Params**

  ```json
  {
    "files": {
      "js": ["js/bob.js"]
    }
  }
  ```

- **Success Response:**

  - **Code:** 200 OK
  - **Content:**

    ```json
    {
      "files": {
        "js": ["js/bob.js"]
      }
    }
    ```

- **Error Response:**

  - **Code:** 404 NOT FOUND
  - **Content:** `{ error : "Release not found" }`

  OR

  - **Code:** 401 UNAUTHORIZED
  - **Content:** `{ error : "Authentication credentials were not provided." }`

---

### Notes

- Replace `your_token_here` with your actual authentication token when making requests.
- Dates and times should be provided in ISO 8601 format.

### Conclusion

These endpoints provide essential functionalities for managing software releases via our API. For further assistance or additional features, please contact our support team.
