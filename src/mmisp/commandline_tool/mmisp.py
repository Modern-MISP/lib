import fire


def create_user(email: str, password: str, role: str ='user') -> str:
  """create-user <email> <password> [-r <role>]"""
  return 'User created with role: {} email: {} and password: {}'.format(role, email, password)

def change_password(email: str, password: str) -> str:
  """change-password <email> <password>"""
  return 'Password changed for user with email: {}'.format(email)

def change_email(email: str , new_email: str) -> str:
  """change-email <email> <new_email>"""
  return 'Email changed for user with email: {} to {}'.format(email, new_email)

def change_role(email: str, role: str) -> str:
  """change-role <email> <role>"""
  return 'Role changed for user with email: {} to {}'.format(email, role)

def create_backup(path: str) -> str:
  """create-backup <path>"""
  return 'Created backup to path: {}'.format(path)

def update_backup() -> str:
  """update-backup"""
  return 'Successfully updated backup'

if __name__ == '__main__':
  fire.Fire({
    'create-user': create_user,
    'change-password': change_password,
    'change-email': change_email,
    'change-role': change_role
    'create-backup': create_backup
    'update-backup': update_backup
  })
