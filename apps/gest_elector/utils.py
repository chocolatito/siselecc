
def vname_f(_meta, field):
    return _meta.get_field(field).verbose_name.title()
