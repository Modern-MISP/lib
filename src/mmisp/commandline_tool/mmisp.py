import fire

# This is a simple command line tool that uses the fire library to create a command line tool for creating users
# and organisations and changing their details.


def create_user(email: str, password: str, role: str = "user") -> str:
    """create-user <email> <password> [-r <role>]"""
    return "User created with role: {} email: {} and password: {}".format(role, email, password)


def create_organisation(
    name: str,
    admin_email: str,
    description: str,
    type: str,
    nationality: str,
    sector: str,
    contacts_email: str,
    local: bool,
    restricted_domain: str,
    landingpage: str,
) -> str:
    """create-organisation <name> <admin_email> <description> <type> <nationality> <sector> <contacts_email> <local>
    <restricted_domain> <landingpage>"""
    output = (
        "Organisation created with name: {} admin_email: {} description: {} type: {} nationality: {} sector: {}"
        + " contacts_email: {} local: {} restricted_domain: {} landingpage: {} "
    )
    return output.format(
        name, admin_email, description, type, nationality, sector, contacts_email, local, restricted_domain, landingpage
    )


def change_password(email: str, password: str) -> str:
    """change-password <email> <password>"""
    return "Password changed for user with email: {}".format(email)


def change_email(email: str, new_email: str) -> str:
    """change-email <email> <new_email>"""
    return "Email changed for user with email: {} to {}".format(email, new_email)


def change_role(email: str, role: str) -> str:
    """change-role <email> <role>"""
    return "Role changed for user with email: {} to {}".format(email, role)


def edit_organisation(
    name: str = None,
    admin_email: str = None,
    description: str = None,
    type: str = None,
    nationality: str = None,
    sector: str = None,
    contacts_email: str = None,
    local: bool = None,
    restricted_domain: str = None,
    landingpage: str = None,
) -> str:
    """edit-oranisation [ <name>] [<admin_email>] [<description>] [-t <type>] [<nationality>] [<sector>] [<contacts_email>]
    [<local>] [<restricted_domain>] [<landingpage>]"""
    output = (
        "organisation edited with name: {} admin_email: {} description: {} type: {} nationality: {} sector: {} "
        + "contacts_email: {} local: {} restricted_domain: {} landingpage: {}"
    )
    return output.format(
        name, admin_email, description, type, nationality, sector, contacts_email, local, restricted_domain, landingpage
    )


def delete_organisation(name: str, admin_email: str) -> str:
    """delete-organisation <name> <admin_email>"""
    return "organisation deleted with name: {} and admin_email: {}".format(name, admin_email)


if __name__ == "__main__":
    fire.Fire(
        {
            "create-user": create_user,
            "create-organisation": create_organisation,
            "change-password": change_password,
            "change-email": change_email,
            "change-role": change_role,
            "edit-organisation": edit_organisation,
            "delete-organisation": delete_organisation,
        }
    )