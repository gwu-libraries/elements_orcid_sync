# elements_orcid_sync

This app will provide the ability to:

1. Extract Symplectic Elements (SE) profile information for a user (as XML)
2. Transform, where possible, certain SE profile entities into equivalent ORCID entities
3. Write ORCiD entities to the user's ORCiD profile.

The app will be able to use ORCiD user tokens collected via the [orcid-integration](https://github.com/gwu-libraries/orcid-integration) app;
the app will use these tokens (when enabled) to write to the users' ORCiD profiles.

So far, the app contains an `add-membership` route which can successfully write a membership object to a user's ORCiD profile.
Other ORCiD write endpoints should work in a similar fashion.

The app also contains a `db-test` route just to confirm that it can connect to the database running in another container.  If we fold this app into the [orcid-integration](https://github.com/gwu-libraries/orcid-integration) app then we can read from the token database.

Here is an example request curl'ed to the `add-membership` route.  Note that the sample membership data json was 
copied from https://github.com/ORCID/orcid-model/blob/master/src/main/resources/record_3.0/samples/write_samples/membership-3.0.json where other entity data samples are available.

```
curl -X POST -H "Content-Type: application/json" -d '{
  "orcid_id": "0009-0008-7777-9999",
  "membership": {
    "department-name": "Department",
    "role-title": "Role",
    "start-date": {
        "year": {
        "value": "2021"
        },
        "month": {
        "value": "02"
        },
        "day": {
        "value": "02"
        }
    },
    "end-date": {
        "year": {
        "value": "2023"
        },
        "month": {
        "value": "01"
        },
        "day": {
        "value": "02"
        }
    },
    "organization": {
        "name": "Research Data Alliance",
        "address": {
        "city": "Dublin",
        "region": "Province of Leinster",
        "country": "IE"
        },
        "disambiguated-organization": {
        "disambiguated-organization-identifier": "https://ror.org/05dc6w374",
        "disambiguation-source": "ROR"
        }
    },
    "url": {
        "value": "http://tempuri.org"
    },
    "external-ids": {
        "external-id": [
        {
            "external-id-type": "grant_number",
            "external-id-value": "external-identifier-value",
            "external-id-url": {
            "value": "http://tempuri.org"
            },
            "external-id-relationship": "self"
        },
        {
            "external-id-type": "grant_number",
            "external-id-value": "external-identifier-value2",
            "external-id-url": {
            "value": "http://tempuri.org/2"
            },
            "external-id-relationship": "self"
        }
        ]
    }
  }
}' http://localhost:8000/add-membership
```
