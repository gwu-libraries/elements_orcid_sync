# elements_orcid_sync

This app will provide the ability to:

1. Extract Symplectic Elements (SE) profile information for a user (as XML)
2. Transform, where possible, certain SE profile entities into equivalent ORCID entities
3. Perform the following interactions with ORCiD profiles:
   - Get data from a user's ORCiD profile
   - Write entities to a user's ORCiD profile
   - Delete entities from a user's ORCiD profile (note that this is only allowed if *this* integration created the entities)

The app will be able to use ORCiD user tokens collected via the [orcid-integration](https://github.com/gwu-libraries/orcid-integration) app;
the app will use these tokens (when enabled) to write to the users' ORCiD profiles.  Currently the tokens must be included in the
payload that is `curl`ed to this app's API

So far, the app contains routes for `get_activities`, `add_activity` and `delete_activity`.  See sample requests for each of these in `sample*.txt`.

The app also contains a `db-test` route just to confirm that it can connect to the database running in another container.  If we fold this app into the [orcid-integration](https://github.com/gwu-libraries/orcid-integration) app then we can read from the token database.