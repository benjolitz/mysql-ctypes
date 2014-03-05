# from ctypes import string_at, create_string_buffer

from MySQLdb import libmysql


# def string_literal(obj):
#     obj = str(obj)
#     buf = create_string_buffer(len(obj) * 2)
#     length = libmysql.c.mysql_escape_string(buf, obj, len(obj))
#     return "'%s'" % string_at(buf, length)

def string_literal(obj):
    source_string = libmysql.ffi.new('char []', str(obj))
    result_string = libmysql.ffi.new('char *')
    buf = libmysql.ffi.buffer(result_string, len(obj)*2)
    length = libmysql.c.mysql_escape_string(buf, source_string, len(obj))
    result = ''.join(buf[index] for index in xrange(length))
    return "'%s'" % result
