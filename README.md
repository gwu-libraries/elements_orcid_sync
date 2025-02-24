# elements_orcid_sync

This app will provide the ability to:

1. Extract Symplectic Elements (SE) profile information for a user (as XML)
2. Transform, where possible, certain SE profile entities into equivalent ORCID entities
3. Write ORCiD entities to the user's ORCiD profile.

The app will be able to use ORCiD user tokens collected via the https://github.com/gwu-libraries/orcid-integration app;
the app will use these tokens (when enabled) to write to the users' ORCiD profiles.

So far, the app contains an `add-membership` route which can successfully write a membership object to a user's ORCiD profile.
Other ORCiD write endpoints should work in a similar fashion.

Here is an example request curl'ed to the `add-membership` route:

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
