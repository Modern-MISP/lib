from collections import defaultdict
from enum import StrEnum
from typing import Literal, Union


class AttributeCategories(StrEnum):
    PAYLOAD_DELIVERY = "Payload delivery"
    ARTIFACTS_DROPPED = "Artifacts dropped"
    PAYLOAD_INSTALLATION = "Payload installation"
    EXTERNAL_ANALYSIS = "External analysis"
    PERSISTENCE_MECHANISM = "Persistence mechanism"
    NETWORK_ACTIVITY = "Network activity"
    ATTRIBUTION = "Attribution"
    SOCIAL_NETWORK = "Social network"
    PERSON = "Person"
    OTHER = "Other"
    INTERNAL_REFERENCE = "Internal reference"
    ANTIVIRUS_DETECTION = "Antivirus detection"
    SUPPORT_TOOL = "Support Tool"
    TARGETING_DATA = "Targeting data"
    PAYLOAD_TYPE = "Payload type"
    FINANCIAL_FRAUD = "Financial fraud"


mapper_val_safe_clsname = {
    "md5": "Md5",
    "sha1": "Sha1",
    "sha256": "Sha256",
    "filename": "Filename",
    "pdb": "Pdb",
    "filename|sha1": "FilenameSha1",
    "filename|sha256": "FilenameSha256",
    "ip-src": "IpSrc",
    "ip-dst": "IpDst",
    "hostname": "Hostname",
    "domain": "Domain",
    "domain|ip": "DomainIp",
    "email": "Email",
    "email-src": "EmailSrc",
    "email-dst": "EmailDst",
    "email-subject": "EmailSubject",
    "email-attachment": "EmailAttachment",
    "email-body": "EmailBody",
    "eppn": "Eppn",
    "float": "Float",
    "git-commit-id": "GitCommitId",
    "url": "Url",
    "http-method": "HttpMethod",
    "user-agent": "UserAgent",
    "ja3-fingerprint-md5": "Ja3FingerprintMd5",
    "jarm-fingerprint": "JarmFingerprint",
    "favicon-mmh3": "FaviconMmh3",
    "hassh-md5": "HasshMd5",
    "hasshserver-md5": "HasshserverMd5",
    "regkey": "Regkey",
    "regkey|value": "RegkeyValue",
    "AS": "As",
    "bro": "Bro",
    "zeek": "Zeek",
    "community-id": "CommunityId",
    "pattern-in-file": "PatternInFile",
    "aba-rtn": "AbaRtn",
    "anonymised": "Anonymised",
    "attachment": "Attachment",
    "authentihash": "Authentihash",
    "azure-application-id": "AzureApplicationId",
    "bank-account-nr": "BankAccountNr",
    "bic": "Bic",
    "bin": "Bin",
    "boolean": "Boolean",
    "btc": "Btc",
    "campaign-id": "CampaignId",
    "campaign-name": "CampaignName",
    "cc-number": "CcNumber",
    "cdhash": "Cdhash",
    "chrome-extension-id": "ChromeExtensionId",
    "comment": "Comment",
    "cookie": "Cookie",
    "cortex": "Cortex",
    "counter": "Counter",
    "country-of-residence": "CountryOfResidence",
    "cpe": "Cpe",
    "dash": "Dash",
    "datetime": "Datetime",
    "date-of-birth": "DateOfBirth",
    "dkim": "Dkim",
    "dkim-signature": "DkimSignature",
    "dns-soa-email": "DnsSoaEmail",
    "email-dst-display-name": "EmailDstDisplayName",
    "email-header": "EmailHeader",
    "email-message-id": "EmailMessageId",
    "email-mime-boundary": "EmailMimeBoundary",
    "email-reply-to": "EmailReplyTo",
    "email-src-display-name": "EmailSrcDisplayName",
    "email-thread-index": "EmailThreadIndex",
    "email-x-mailer": "EmailXMailer",
    "filename|authentihash": "FilenameAuthentihash",
    "filename|impfuzzy": "FilenameImpfuzzy",
    "filename|imphash": "FilenameImphash",
    "filename|md5": "FilenameMd5",
    "filename-pattern": "FilenamePattern",
    "filename|pehash": "FilenamePehash",
    "filename|sha224": "FilenameSha224",
    "filename|sha384": "FilenameSha384",
    "filename|sha3-224": "FilenameSha3224",
    "filename|sha3-256": "FilenameSha3256",
    "filename|sha3-384": "FilenameSha3384",
    "filename|sha3-512": "FilenameSha3512",
    "filename|sha512": "FilenameSha512",
    "filename|sha512/224": "FilenameSha512224",
    "filename|sha512/256": "FilenameSha512256",
    "filename|ssdeep": "FilenameSsdeep",
    "filename|tlsh": "FilenameTlsh",
    "filename|vhash": "FilenameVhash",
    "first-name": "FirstName",
    "frequent-flyer-number": "FrequentFlyerNumber",
    "full-name": "FullName",
    "gender": "Gender",
    "gene": "Gene",
    "github-organisation": "GithubOrganisation",
    "github-repository": "GithubRepository",
    "github-username": "GithubUsername",
    "hex": "Hex",
    "hostname|port": "HostnamePort",
    "iban": "Iban",
    "identity-card-number": "IdentityCardNumber",
    "impfuzzy": "Impfuzzy",
    "imphash": "Imphash",
    "ip-dst|port": "IpDstPort",
    "ip-src|port": "IpSrcPort",
    "issue-date-of-the-visa": "IssueDateOfTheVisa",
    "jabber-id": "JabberId",
    "kusto-query": "KustoQuery",
    "last-name": "LastName",
    "link": "Link",
    "mac-address": "MacAddress",
    "mac-eui-64": "MacEui64",
    "malware-sample": "MalwareSample",
    "malware-type": "MalwareType",
    "middle-name": "MiddleName",
    "mime-type": "MimeType",
    "mobile-application-id": "MobileApplicationId",
    "mutex": "Mutex",
    "named pipe": "NamedPipe",
    "nationality": "Nationality",
    "other": "Other",
    "passenger-name-record-locator-number": "PassengerNameRecordLocatorNumber",
    "passport-country": "PassportCountry",
    "passport-expiration": "PassportExpiration",
    "passport-number": "PassportNumber",
    "pattern-in-memory": "PatternInMemory",
    "pattern-in-traffic": "PatternInTraffic",
    "payment-details": "PaymentDetails",
    "pehash": "Pehash",
    "pgp-private-key": "PgpPrivateKey",
    "pgp-public-key": "PgpPublicKey",
    "phone-number": "PhoneNumber",
    "place-of-birth": "PlaceOfBirth",
    "place-port-of-clearance": "PlacePortOfClearance",
    "place-port-of-onward-foreign-destination": "PlacePortOfOnwardForeignDestination",
    "place-port-of-original-embarkation": "PlacePortOfOriginalEmbarkation",
    "port": "Port",
    "primary-residence": "PrimaryResidence",
    "process-state": "ProcessState",
    "prtn": "Prtn",
    "redress-number": "RedressNumber",
    "sha224": "Sha224",
    "sha384": "Sha384",
    "sha3-224": "Sha3224",
    "sha3-256": "Sha3256",
    "sha3-384": "Sha3384",
    "sha3-512": "Sha3512",
    "sha512": "Sha512",
    "sha512/224": "Sha512224",
    "sha512/256": "Sha512256",
    "sigma": "Sigma",
    "size-in-bytes": "SizeInBytes",
    "snort": "Snort",
    "special-service-request": "SpecialServiceRequest",
    "ssdeep": "Ssdeep",
    "ssh-fingerprint": "SshFingerprint",
    "stix2-pattern": "Stix2Pattern",
    "target-email": "TargetEmail",
    "target-external": "TargetExternal",
    "target-location": "TargetLocation",
    "target-machine": "TargetMachine",
    "target-org": "TargetOrg",
    "target-user": "TargetUser",
    "telfhash": "Telfhash",
    "text": "Text",
    "threat-actor": "ThreatActor",
    "tlsh": "Tlsh",
    "travel-details": "TravelDetails",
    "twitter-id": "TwitterId",
    "uri": "Uri",
    "vhash": "Vhash",
    "visa-number": "VisaNumber",
    "vulnerability": "Vulnerability",
    "weakness": "Weakness",
    "whois-creation-date": "WhoisCreationDate",
    "whois-registrant-email": "WhoisRegistrantEmail",
    "whois-registrant-name": "WhoisRegistrantName",
    "whois-registrant-org": "WhoisRegistrantOrg",
    "whois-registrant-phone": "WhoisRegistrantPhone",
    "whois-registrar": "WhoisRegistrar",
    "windows-scheduled-task": "WindowsScheduledTask",
    "windows-service-displayname": "WindowsServiceDisplayname",
    "windows-service-name": "WindowsServiceName",
    "x509-fingerprint-md5": "X509FingerprintMd5",
    "x509-fingerprint-sha1": "X509FingerprintSha1",
    "x509-fingerprint-sha256": "X509FingerprintSha256",
    "xmr": "Xmr",
    "yara": "Yara",
}

mapper_safe_clsname_val = dict((v, k) for k, v in mapper_val_safe_clsname.items())
literal_valid_attribute_types = Union[*[Literal[k] for k in mapper_val_safe_clsname.keys()]]

default_category = {
    "md5": AttributeCategories.PAYLOAD_DELIVERY,
    "sha1": AttributeCategories.PAYLOAD_DELIVERY,
    "sha256": AttributeCategories.PAYLOAD_DELIVERY,
    "filename": AttributeCategories.PAYLOAD_DELIVERY,
    "pdb": AttributeCategories.ARTIFACTS_DROPPED,
    "filename|sha1": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha256": AttributeCategories.PAYLOAD_DELIVERY,
    "ip-src": AttributeCategories.NETWORK_ACTIVITY,
    "ip-dst": AttributeCategories.NETWORK_ACTIVITY,
    "hostname": AttributeCategories.NETWORK_ACTIVITY,
    "domain": AttributeCategories.NETWORK_ACTIVITY,
    "domain|ip": AttributeCategories.NETWORK_ACTIVITY,
    "email": AttributeCategories.SOCIAL_NETWORK,
    "email-src": AttributeCategories.PAYLOAD_DELIVERY,
    "email-dst": AttributeCategories.NETWORK_ACTIVITY,
    "email-subject": AttributeCategories.PAYLOAD_DELIVERY,
    "email-attachment": AttributeCategories.PAYLOAD_DELIVERY,
    "email-body": AttributeCategories.PAYLOAD_DELIVERY,
    "eppn": AttributeCategories.NETWORK_ACTIVITY,
    "float": AttributeCategories.OTHER,
    "git-commit-id": AttributeCategories.INTERNAL_REFERENCE,
    "url": AttributeCategories.NETWORK_ACTIVITY,
    "http-method": AttributeCategories.NETWORK_ACTIVITY,
    "user-agent": AttributeCategories.NETWORK_ACTIVITY,
    "ja3-fingerprint-md5": AttributeCategories.NETWORK_ACTIVITY,
    "jarm-fingerprint": AttributeCategories.NETWORK_ACTIVITY,
    "favicon-mmh3": AttributeCategories.NETWORK_ACTIVITY,
    "hassh-md5": AttributeCategories.NETWORK_ACTIVITY,
    "hasshserver-md5": AttributeCategories.NETWORK_ACTIVITY,
    "regkey": AttributeCategories.PERSISTENCE_MECHANISM,
    "regkey|value": AttributeCategories.PERSISTENCE_MECHANISM,
    "AS": AttributeCategories.NETWORK_ACTIVITY,
    "bro": AttributeCategories.NETWORK_ACTIVITY,
    "zeek": AttributeCategories.NETWORK_ACTIVITY,
    "community-id": AttributeCategories.NETWORK_ACTIVITY,
    "pattern-in-file": AttributeCategories.PAYLOAD_INSTALLATION,
    "aba-rtn": AttributeCategories.FINANCIAL_FRAUD,
    "anonymised": AttributeCategories.OTHER,
    "attachment": AttributeCategories.EXTERNAL_ANALYSIS,
    "authentihash": AttributeCategories.PAYLOAD_DELIVERY,
    "azure-application-id": AttributeCategories.PAYLOAD_DELIVERY,
    "bank-account-nr": AttributeCategories.FINANCIAL_FRAUD,
    "bic": AttributeCategories.FINANCIAL_FRAUD,
    "bin": AttributeCategories.FINANCIAL_FRAUD,
    "boolean": AttributeCategories.OTHER,
    "btc": AttributeCategories.FINANCIAL_FRAUD,
    "campaign-id": AttributeCategories.ATTRIBUTION,
    "campaign-name": AttributeCategories.ATTRIBUTION,
    "cc-number": AttributeCategories.FINANCIAL_FRAUD,
    "cdhash": AttributeCategories.PAYLOAD_DELIVERY,
    "chrome-extension-id": AttributeCategories.PAYLOAD_DELIVERY,
    "comment": AttributeCategories.OTHER,
    "cookie": AttributeCategories.NETWORK_ACTIVITY,
    "cortex": AttributeCategories.EXTERNAL_ANALYSIS,
    "counter": AttributeCategories.OTHER,
    "country-of-residence": AttributeCategories.PERSON,
    "cpe": AttributeCategories.EXTERNAL_ANALYSIS,
    "dash": AttributeCategories.FINANCIAL_FRAUD,
    "datetime": AttributeCategories.OTHER,
    "date-of-birth": AttributeCategories.PERSON,
    "dkim": AttributeCategories.NETWORK_ACTIVITY,
    "dkim-signature": AttributeCategories.NETWORK_ACTIVITY,
    "dns-soa-email": AttributeCategories.ATTRIBUTION,
    "email-dst-display-name": AttributeCategories.PAYLOAD_DELIVERY,
    "email-header": AttributeCategories.PAYLOAD_DELIVERY,
    "email-message-id": AttributeCategories.PAYLOAD_DELIVERY,
    "email-mime-boundary": AttributeCategories.PAYLOAD_DELIVERY,
    "email-reply-to": AttributeCategories.PAYLOAD_DELIVERY,
    "email-src-display-name": AttributeCategories.PAYLOAD_DELIVERY,
    "email-thread-index": AttributeCategories.PAYLOAD_DELIVERY,
    "email-x-mailer": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|authentihash": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|impfuzzy": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|imphash": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|md5": AttributeCategories.PAYLOAD_DELIVERY,
    "filename-pattern": AttributeCategories.PAYLOAD_INSTALLATION,
    "filename|pehash": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha224": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha384": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha3-224": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha3-256": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha3-384": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha3-512": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha512": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha512/224": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|sha512/256": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|ssdeep": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|tlsh": AttributeCategories.PAYLOAD_DELIVERY,
    "filename|vhash": AttributeCategories.PAYLOAD_DELIVERY,
    "first-name": AttributeCategories.PERSON,
    "frequent-flyer-number": AttributeCategories.PERSON,
    "full-name": AttributeCategories.PERSON,
    "gender": AttributeCategories.PERSON,
    "gene": AttributeCategories.ARTIFACTS_DROPPED,
    "github-organisation": AttributeCategories.SOCIAL_NETWORK,
    "github-repository": AttributeCategories.SOCIAL_NETWORK,
    "github-username": AttributeCategories.SOCIAL_NETWORK,
    "hex": AttributeCategories.OTHER,
    "hostname|port": AttributeCategories.NETWORK_ACTIVITY,
    "iban": AttributeCategories.FINANCIAL_FRAUD,
    "identity-card-number": AttributeCategories.PERSON,
    "impfuzzy": AttributeCategories.PAYLOAD_DELIVERY,
    "imphash": AttributeCategories.PAYLOAD_DELIVERY,
    "ip-dst|port": AttributeCategories.NETWORK_ACTIVITY,
    "ip-src|port": AttributeCategories.NETWORK_ACTIVITY,
    "issue-date-of-the-visa": AttributeCategories.PERSON,
    "jabber-id": AttributeCategories.SOCIAL_NETWORK,
    "kusto-query": AttributeCategories.ARTIFACTS_DROPPED,
    "last-name": AttributeCategories.PERSON,
    "link": AttributeCategories.EXTERNAL_ANALYSIS,
    "mac-address": AttributeCategories.NETWORK_ACTIVITY,
    "mac-eui-64": AttributeCategories.NETWORK_ACTIVITY,
    "malware-sample": AttributeCategories.PAYLOAD_DELIVERY,
    "malware-type": AttributeCategories.PAYLOAD_DELIVERY,
    "middle-name": AttributeCategories.PERSON,
    "mime-type": AttributeCategories.ARTIFACTS_DROPPED,
    "mobile-application-id": AttributeCategories.PAYLOAD_DELIVERY,
    "mutex": AttributeCategories.ARTIFACTS_DROPPED,
    "named pipe": AttributeCategories.ARTIFACTS_DROPPED,
    "nationality": AttributeCategories.PERSON,
    "other": AttributeCategories.OTHER,
    "passenger-name-record-locator-number": AttributeCategories.PERSON,
    "passport-country": AttributeCategories.PERSON,
    "passport-expiration": AttributeCategories.PERSON,
    "passport-number": AttributeCategories.PERSON,
    "pattern-in-memory": AttributeCategories.PAYLOAD_INSTALLATION,
    "pattern-in-traffic": AttributeCategories.NETWORK_ACTIVITY,
    "payment-details": AttributeCategories.PERSON,
    "pehash": AttributeCategories.PAYLOAD_DELIVERY,
    "pgp-private-key": AttributeCategories.PERSON,
    "pgp-public-key": AttributeCategories.PERSON,
    "phone-number": AttributeCategories.PERSON,
    "place-of-birth": AttributeCategories.PERSON,
    "place-port-of-clearance": AttributeCategories.PERSON,
    "place-port-of-onward-foreign-destination": AttributeCategories.PERSON,
    "place-port-of-original-embarkation": AttributeCategories.PERSON,
    "port": AttributeCategories.NETWORK_ACTIVITY,
    "primary-residence": AttributeCategories.PERSON,
    "process-state": AttributeCategories.ARTIFACTS_DROPPED,
    "prtn": AttributeCategories.FINANCIAL_FRAUD,
    "redress-number": AttributeCategories.PERSON,
    "sha224": AttributeCategories.PAYLOAD_DELIVERY,
    "sha384": AttributeCategories.PAYLOAD_DELIVERY,
    "sha3-224": AttributeCategories.PAYLOAD_DELIVERY,
    "sha3-256": AttributeCategories.PAYLOAD_DELIVERY,
    "sha3-384": AttributeCategories.PAYLOAD_DELIVERY,
    "sha3-512": AttributeCategories.PAYLOAD_DELIVERY,
    "sha512": AttributeCategories.PAYLOAD_DELIVERY,
    "sha512/224": AttributeCategories.PAYLOAD_DELIVERY,
    "sha512/256": AttributeCategories.PAYLOAD_DELIVERY,
    "sigma": AttributeCategories.PAYLOAD_INSTALLATION,
    "size-in-bytes": AttributeCategories.OTHER,
    "snort": AttributeCategories.NETWORK_ACTIVITY,
    "special-service-request": AttributeCategories.PERSON,
    "ssdeep": AttributeCategories.PAYLOAD_DELIVERY,
    "ssh-fingerprint": AttributeCategories.NETWORK_ACTIVITY,
    "stix2-pattern": AttributeCategories.PAYLOAD_INSTALLATION,
    "target-email": AttributeCategories.TARGETING_DATA,
    "target-external": AttributeCategories.TARGETING_DATA,
    "target-location": AttributeCategories.TARGETING_DATA,
    "target-machine": AttributeCategories.TARGETING_DATA,
    "target-org": AttributeCategories.TARGETING_DATA,
    "target-user": AttributeCategories.TARGETING_DATA,
    "telfhash": AttributeCategories.PAYLOAD_DELIVERY,
    "text": AttributeCategories.OTHER,
    "threat-actor": AttributeCategories.ATTRIBUTION,
    "tlsh": AttributeCategories.PAYLOAD_DELIVERY,
    "travel-details": AttributeCategories.PERSON,
    "twitter-id": AttributeCategories.SOCIAL_NETWORK,
    "uri": AttributeCategories.NETWORK_ACTIVITY,
    "vhash": AttributeCategories.PAYLOAD_DELIVERY,
    "visa-number": AttributeCategories.PERSON,
    "vulnerability": AttributeCategories.EXTERNAL_ANALYSIS,
    "weakness": AttributeCategories.EXTERNAL_ANALYSIS,
    "whois-creation-date": AttributeCategories.ATTRIBUTION,
    "whois-registrant-email": AttributeCategories.ATTRIBUTION,
    "whois-registrant-name": AttributeCategories.ATTRIBUTION,
    "whois-registrant-org": AttributeCategories.ATTRIBUTION,
    "whois-registrant-phone": AttributeCategories.ATTRIBUTION,
    "whois-registrar": AttributeCategories.ATTRIBUTION,
    "windows-scheduled-task": AttributeCategories.ARTIFACTS_DROPPED,
    "windows-service-displayname": AttributeCategories.ARTIFACTS_DROPPED,
    "windows-service-name": AttributeCategories.ARTIFACTS_DROPPED,
    "x509-fingerprint-md5": AttributeCategories.NETWORK_ACTIVITY,
    "x509-fingerprint-sha1": AttributeCategories.NETWORK_ACTIVITY,
    "x509-fingerprint-sha256": AttributeCategories.NETWORK_ACTIVITY,
    "xmr": AttributeCategories.FINANCIAL_FRAUD,
    "yara": AttributeCategories.PAYLOAD_INSTALLATION,
}

categories = {
    "aba-rtn": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "anonymised": frozenset(
        {
            AttributeCategories.TARGETING_DATA,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.PERSON,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "AS": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "attachment": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "authentihash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "azure-application-id": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}),
    "bank-account-nr": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "bic": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "bin": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "boolean": frozenset({AttributeCategories.OTHER}),
    "bro": frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    "btc": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "campaign-id": frozenset({AttributeCategories.ATTRIBUTION}),
    "campaign-name": frozenset({AttributeCategories.ATTRIBUTION}),
    "cc-number": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "cdhash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "chrome-extension-id": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}),
    "comment": frozenset(
        {
            AttributeCategories.TARGETING_DATA,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.PERSON,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "community-id": frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    "cookie": frozenset({AttributeCategories.ARTIFACTS_DROPPED, AttributeCategories.NETWORK_ACTIVITY}),
    "cortex": frozenset({AttributeCategories.EXTERNAL_ANALYSIS}),
    "counter": frozenset({AttributeCategories.OTHER}),
    "country-of-residence": frozenset({AttributeCategories.PERSON}),
    "cpe": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.OTHER,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "dash": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "datetime": frozenset({AttributeCategories.OTHER}),
    "date-of-birth": frozenset({AttributeCategories.PERSON}),
    "dkim": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "dkim-signature": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "dns-soa-email": frozenset({AttributeCategories.ATTRIBUTION}),
    "domain": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "domain|ip": frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    "email": frozenset(
        {
            AttributeCategories.PERSON,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "email-attachment": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-body": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-dst": frozenset(
        {AttributeCategories.SOCIAL_NETWORK, AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}
    ),
    "email-dst-display-name": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-header": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-message-id": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-mime-boundary": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-reply-to": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-src": frozenset(
        {AttributeCategories.SOCIAL_NETWORK, AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}
    ),
    "email-src-display-name": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-subject": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}),
    "email-thread-index": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "email-x-mailer": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "eppn": frozenset({AttributeCategories.SOCIAL_NETWORK, AttributeCategories.NETWORK_ACTIVITY}),
    "favicon-mmh3": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "filename": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
        }
    ),
    "filename|authentihash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|impfuzzy": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|imphash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|md5": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename-pattern": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "filename|pehash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha1": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha224": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha384": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha3-224": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha3-256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha3-384": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha3-512": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha512": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha512/224": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|sha512/256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|ssdeep": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|tlsh": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "filename|vhash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "first-name": frozenset({AttributeCategories.PERSON}),
    "float": frozenset({AttributeCategories.OTHER}),
    "frequent-flyer-number": frozenset({AttributeCategories.PERSON}),
    "full-name": frozenset({AttributeCategories.PERSON}),
    "gender": frozenset({AttributeCategories.PERSON}),
    "gene": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "github-organisation": frozenset({AttributeCategories.SOCIAL_NETWORK}),
    "github-repository": frozenset({AttributeCategories.SOCIAL_NETWORK, AttributeCategories.EXTERNAL_ANALYSIS}),
    "github-username": frozenset({AttributeCategories.SOCIAL_NETWORK}),
    "git-commit-id": frozenset({AttributeCategories.INTERNAL_REFERENCE}),
    "hasshserver-md5": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "hassh-md5": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "hex": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "hostname": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "hostname|port": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.NETWORK_ACTIVITY}),
    "http-method": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "iban": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "identity-card-number": frozenset({AttributeCategories.PERSON}),
    "impfuzzy": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "imphash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "ip-dst": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "ip-dst|port": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "ip-src": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "ip-src|port": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "issue-date-of-the-visa": frozenset({AttributeCategories.PERSON}),
    "ja3-fingerprint-md5": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "jabber-id": frozenset({AttributeCategories.SOCIAL_NETWORK}),
    "jarm-fingerprint": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "kusto-query": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "last-name": frozenset({AttributeCategories.PERSON}),
    "link": frozenset(
        {
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    "mac-address": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "mac-eui-64": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "malware-sample": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "malware-type": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}),
    "md5": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "middle-name": frozenset({AttributeCategories.PERSON}),
    "mime-type": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "mobile-application-id": frozenset(
        {AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}
    ),
    "mutex": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "named pipe": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "nationality": frozenset({AttributeCategories.PERSON}),
    "other": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.PERSON,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "passenger-name-record-locator-number": frozenset({AttributeCategories.PERSON}),
    "passport-country": frozenset({AttributeCategories.PERSON}),
    "passport-expiration": frozenset({AttributeCategories.PERSON}),
    "passport-number": frozenset({AttributeCategories.PERSON}),
    "pattern-in-file": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "pattern-in-memory": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    "pattern-in-traffic": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "payment-details": frozenset({AttributeCategories.PERSON}),
    "pdb": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "pehash": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}),
    "pgp-private-key": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PERSON,
            AttributeCategories.OTHER,
        }
    ),
    "pgp-public-key": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PERSON,
            AttributeCategories.OTHER,
        }
    ),
    "phone-number": frozenset(
        {AttributeCategories.FINANCIAL_FRAUD, AttributeCategories.PERSON, AttributeCategories.OTHER}
    ),
    "place-of-birth": frozenset({AttributeCategories.PERSON}),
    "place-port-of-clearance": frozenset({AttributeCategories.PERSON}),
    "place-port-of-onward-foreign-destination": frozenset({AttributeCategories.PERSON}),
    "place-port-of-original-embarkation": frozenset({AttributeCategories.PERSON}),
    "port": frozenset({AttributeCategories.OTHER, AttributeCategories.NETWORK_ACTIVITY}),
    "primary-residence": frozenset({AttributeCategories.PERSON}),
    "process-state": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "prtn": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "redress-number": frozenset({AttributeCategories.PERSON}),
    "regkey": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    "regkey|value": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.EXTERNAL_ANALYSIS,
        }
    ),
    "sha1": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha224": frozenset({AttributeCategories.PAYLOAD_DELIVERY}),
    "sha256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha384": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha3-224": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha3-256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha3-384": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha3-512": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha512": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha512/224": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sha512/256": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "sigma": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "size-in-bytes": frozenset({AttributeCategories.OTHER}),
    "snort": frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
    "special-service-request": frozenset({AttributeCategories.PERSON}),
    "ssdeep": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "ssh-fingerprint": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "stix2-pattern": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.NETWORK_ACTIVITY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "target-email": frozenset({AttributeCategories.TARGETING_DATA}),
    "target-external": frozenset({AttributeCategories.TARGETING_DATA}),
    "target-location": frozenset({AttributeCategories.TARGETING_DATA}),
    "target-machine": frozenset({AttributeCategories.TARGETING_DATA}),
    "target-org": frozenset({AttributeCategories.TARGETING_DATA}),
    "target-user": frozenset({AttributeCategories.TARGETING_DATA}),
    "telfhash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "text": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.INTERNAL_REFERENCE,
            AttributeCategories.PAYLOAD_TYPE,
            AttributeCategories.PERSISTENCE_MECHANISM,
            AttributeCategories.FINANCIAL_FRAUD,
            AttributeCategories.PERSON,
            AttributeCategories.SUPPORT_TOOL,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.SOCIAL_NETWORK,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.ANTIVIRUS_DETECTION,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.OTHER,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "threat-actor": frozenset({AttributeCategories.ATTRIBUTION}),
    "tlsh": frozenset({AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.PAYLOAD_INSTALLATION}),
    "travel-details": frozenset({AttributeCategories.PERSON}),
    "twitter-id": frozenset({AttributeCategories.SOCIAL_NETWORK}),
    "uri": frozenset({AttributeCategories.NETWORK_ACTIVITY}),
    "url": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "user-agent": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "vhash": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "visa-number": frozenset({AttributeCategories.PERSON}),
    "vulnerability": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "weakness": frozenset(
        {
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "whois-creation-date": frozenset({AttributeCategories.ATTRIBUTION}),
    "whois-registrant-email": frozenset(
        {AttributeCategories.ATTRIBUTION, AttributeCategories.PAYLOAD_DELIVERY, AttributeCategories.SOCIAL_NETWORK}
    ),
    "whois-registrant-name": frozenset({AttributeCategories.ATTRIBUTION}),
    "whois-registrant-org": frozenset({AttributeCategories.ATTRIBUTION}),
    "whois-registrant-phone": frozenset({AttributeCategories.ATTRIBUTION}),
    "whois-registrar": frozenset({AttributeCategories.ATTRIBUTION}),
    "windows-scheduled-task": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "windows-service-displayname": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "windows-service-name": frozenset({AttributeCategories.ARTIFACTS_DROPPED}),
    "x509-fingerprint-md5": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "x509-fingerprint-sha1": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "x509-fingerprint-sha256": frozenset(
        {
            AttributeCategories.PAYLOAD_INSTALLATION,
            AttributeCategories.ATTRIBUTION,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.EXTERNAL_ANALYSIS,
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.NETWORK_ACTIVITY,
        }
    ),
    "xmr": frozenset({AttributeCategories.FINANCIAL_FRAUD}),
    "yara": frozenset(
        {
            AttributeCategories.ARTIFACTS_DROPPED,
            AttributeCategories.PAYLOAD_DELIVERY,
            AttributeCategories.PAYLOAD_INSTALLATION,
        }
    ),
    "zeek": frozenset({AttributeCategories.EXTERNAL_ANALYSIS, AttributeCategories.NETWORK_ACTIVITY}),
}

inverted_categories = defaultdict(list)

for key, value in categories.items():
    for category in value:
        inverted_categories[category.value].append(key)


to_ids = {
    "aba-rtn": True,
    "anonymised": False,
    "AS": False,
    "attachment": False,
    "authentihash": True,
    "azure-application-id": True,
    "bank-account-nr": True,
    "bic": True,
    "bin": True,
    "boolean": False,
    "bro": True,
    "btc": True,
    "campaign-id": False,
    "campaign-name": False,
    "cc-number": True,
    "cdhash": True,
    "chrome-extension-id": True,
    "comment": False,
    "community-id": True,
    "cookie": False,
    "cortex": False,
    "counter": False,
    "country-of-residence": False,
    "cpe": False,
    "dash": True,
    "datetime": False,
    "date-of-birth": False,
    "dkim": False,
    "dkim-signature": False,
    "dns-soa-email": False,
    "domain": True,
    "domain|ip": True,
    "email": True,
    "email-attachment": True,
    "email-body": False,
    "email-dst": True,
    "email-dst-display-name": False,
    "email-header": False,
    "email-message-id": False,
    "email-mime-boundary": False,
    "email-reply-to": False,
    "email-src": True,
    "email-src-display-name": False,
    "email-subject": False,
    "email-thread-index": False,
    "email-x-mailer": False,
    "eppn": True,
    "favicon-mmh3": True,
    "filename": True,
    "filename|authentihash": True,
    "filename|impfuzzy": True,
    "filename|imphash": True,
    "filename|md5": True,
    "filename-pattern": True,
    "filename|pehash": True,
    "filename|sha1": True,
    "filename|sha224": True,
    "filename|sha256": True,
    "filename|sha384": True,
    "filename|sha3-224": True,
    "filename|sha3-256": True,
    "filename|sha3-384": True,
    "filename|sha3-512": True,
    "filename|sha512": True,
    "filename|sha512/224": True,
    "filename|sha512/256": True,
    "filename|ssdeep": True,
    "filename|tlsh": True,
    "filename|vhash": True,
    "first-name": False,
    "float": False,
    "frequent-flyer-number": False,
    "full-name": False,
    "gender": False,
    "gene": False,
    "github-organisation": False,
    "github-repository": False,
    "github-username": False,
    "git-commit-id": False,
    "hasshserver-md5": True,
    "hassh-md5": True,
    "hex": False,
    "hostname": True,
    "hostname|port": True,
    "http-method": False,
    "iban": True,
    "identity-card-number": False,
    "impfuzzy": True,
    "imphash": True,
    "ip-dst": True,
    "ip-dst|port": True,
    "ip-src": True,
    "ip-src|port": True,
    "issue-date-of-the-visa": False,
    "ja3-fingerprint-md5": True,
    "jabber-id": False,
    "jarm-fingerprint": True,
    "kusto-query": False,
    "last-name": False,
    "link": False,
    "mac-address": False,
    "mac-eui-64": False,
    "malware-sample": True,
    "malware-type": False,
    "md5": True,
    "middle-name": False,
    "mime-type": False,
    "mobile-application-id": True,
    "mutex": True,
    "named pipe": False,
    "nationality": False,
    "other": False,
    "passenger-name-record-locator-number": False,
    "passport-country": False,
    "passport-expiration": False,
    "passport-number": False,
    "pattern-in-file": True,
    "pattern-in-memory": True,
    "pattern-in-traffic": True,
    "payment-details": False,
    "pdb": False,
    "pehash": True,
    "pgp-private-key": False,
    "pgp-public-key": False,
    "phone-number": False,
    "place-of-birth": False,
    "place-port-of-clearance": False,
    "place-port-of-onward-foreign-destination": False,
    "place-port-of-original-embarkation": False,
    "port": False,
    "primary-residence": False,
    "process-state": False,
    "prtn": True,
    "redress-number": False,
    "regkey": True,
    "regkey|value": True,
    "sha1": True,
    "sha224": True,
    "sha256": True,
    "sha384": True,
    "sha3-224": True,
    "sha3-256": True,
    "sha3-384": True,
    "sha3-512": True,
    "sha512": True,
    "sha512/224": True,
    "sha512/256": True,
    "sigma": True,
    "size-in-bytes": False,
    "snort": True,
    "special-service-request": False,
    "ssdeep": True,
    "ssh-fingerprint": False,
    "stix2-pattern": True,
    "target-email": False,
    "target-external": False,
    "target-location": False,
    "target-machine": False,
    "target-org": False,
    "target-user": False,
    "telfhash": True,
    "text": False,
    "threat-actor": False,
    "tlsh": True,
    "travel-details": False,
    "twitter-id": False,
    "uri": True,
    "url": True,
    "user-agent": False,
    "vhash": True,
    "visa-number": False,
    "vulnerability": False,
    "weakness": False,
    "whois-creation-date": False,
    "whois-registrant-email": False,
    "whois-registrant-name": False,
    "whois-registrant-org": False,
    "whois-registrant-phone": False,
    "whois-registrar": False,
    "windows-scheduled-task": False,
    "windows-service-displayname": False,
    "windows-service-name": False,
    "x509-fingerprint-md5": True,
    "x509-fingerprint-sha1": True,
    "x509-fingerprint-sha256": True,
    "xmr": True,
    "yara": True,
    "zeek": True,
}
