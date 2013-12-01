import collections

# Represents form fields as stored in the form.
JoggerEntry= collections.namedtuple(
    'JoggerEntry',
    'token op entry_id draft_id '
    'title body permalink tags trackback miniblog techblog allow_comments '
    'level notify categories')
