from cffi import FFI


ffi = FFI()
ffi.cdef("""

/* Define the MYSQL_FIELD type */
typedef struct st_mysql_field {
  char *name;                 /* Name of column */
  char *org_name;             /* Original column name, if an alias */
  char *table;                /* Table of column if column was a field */
  char *org_table;            /* Org table name, if table was an alias */
  char *db;                   /* Database for table */
  char *catalog;          /* Catalog for table */
  char *def;                  /* Default value (set by mysql_list_fields) */
  unsigned long length;       /* Width of column (create length) */
  unsigned long max_length;   /* Max width for selected set */
  unsigned int name_length;
  unsigned int org_name_length;
  unsigned int table_length;
  unsigned int org_table_length;
  unsigned int db_length;
  unsigned int catalog_length;
  unsigned int def_length;
  unsigned int flags;         /* Div flags */
  unsigned int decimals;      /* Number of decimals in field */
  unsigned int charsetnr;     /* Character set */
  enum enum_field_types type; /* Type of field. See mysql_com.h for types */
  void *extension;
} MYSQL_FIELD;

/* Unknown if used yet */
typedef char **MYSQL_ROW;       /* return data as array of strings */
typedef unsigned int MYSQL_FIELD_OFFSET; /* offset to current field */
typedef struct st_mysql_rows {
  struct st_mysql_rows *next;       /* list of rows */
  MYSQL_ROW data;
  unsigned long length;
} MYSQL_ROWS;
typedef MYSQL_ROWS *MYSQL_ROW_OFFSET;   /* offset to current row */

typedef char my_bool;
typedef unsigned long long my_ulonglong;

/* Define NET type for MYSQL primary type: */
struct st_vio;                  /* Only C */
typedef struct st_vio Vio;
typedef int my_socket;  /* File descriptor for sockets */

typedef struct st_net {
  Vio *vio;
  unsigned char *buff,*buff_end,*write_pos,*read_pos;
  my_socket fd;                 /* For Perl DBI/dbd */
  /*
    The following variable is set if we are doing several queries in one
    command ( as in LOAD TABLE ... FROM MASTER ),
    and do not want to confuse the client with OK at the wrong time
  */
  unsigned long remain_in_buf,length, buf_length, where_b;
  unsigned long max_packet,max_packet_size;
  unsigned int pkt_nr,compress_pkt_nr;
  unsigned int write_timeout, read_timeout, retry_count;
  int fcntl;
  unsigned int *return_status;
  unsigned char reading_or_writing;
  char save_char;
  my_bool unused1; /* Please remove with the next incompatible ABI change */
  my_bool unused2; /* Please remove with the next incompatible ABI change */
  my_bool compress;
  my_bool unused3; /* Please remove with the next incompatible ABI change. */
  /*
    Pointer to query object in query cache, do not equal NULL (0) for
    queries in cache that have not stored its results yet
  */
  /*
    Unused, please remove with the next incompatible ABI change.
  */
  unsigned char *unused;
  unsigned int last_errno;
  unsigned char error;
  my_bool unused4; /* Please remove with the next incompatible ABI change. */
  my_bool unused5; /* Please remove with the next incompatible ABI change. */
  /** Client library error message buffer. Actually belongs to struct MYSQL. */
  char last_error[512];
  /** Client library sqlstate buffer. Set along with the error message. */
  char sqlstate[6];
  /**
    Extension pointer, for the caller private use.
    Any program linking with the networking library can use this pointer,
    which is handy when private connection specific data needs to be
    maintained.
    The mysqld server process uses this pointer internally,
    to maintain the server internal instrumentation for the connection.
  */
  void *extension;
} NET;

/* Define MEM_ROOT */
typedef unsigned char   uchar;  /* Short for unsigned char */
typedef unsigned int uint;
typedef unsigned short ushort;

typedef struct st_used_mem
{                  /* struct for once_alloc (block) */
  struct st_used_mem *next;    /* Next block in use */
  unsigned int  left;          /* memory left in block  */
  unsigned int  size;          /* size of block */
} USED_MEM;

struct st_dynamic_array;
typedef struct st_dynamic_array
{
  uchar *buffer;
  uint elements,max_element;
  uint alloc_increment;
  uint size_of_element;
} DYNAMIC_ARRAY;

typedef struct st_mem_root
{
  USED_MEM *free;                  /* blocks with free memory in it */
  USED_MEM *used;                  /* blocks almost without free memory */
  USED_MEM *pre_alloc;             /* preallocated block */
  /* if block have less memory it will be put in 'used' list */
  size_t min_malloc;
  size_t block_size;               /* initial block size */
  unsigned int block_num;          /* allocated blocks counter */
  /* 
     first free block in queue test counter (if it exceed 
     MAX_BLOCK_USAGE_BEFORE_DROP block will be dropped in 'used' list)
  */
  unsigned int first_block_usage;

  void (*error_handler)(void);
} MEM_ROOT;

/* Define LIST type for MYSQL type */
typedef struct st_list {
  struct st_list *prev,*next;
  void *data;
} LIST;

enum mysql_status 
{
  MYSQL_STATUS_READY, MYSQL_STATUS_GET_RESULT, MYSQL_STATUS_USE_RESULT,
  MYSQL_STATUS_STATEMENT_GET_RESULT
};

/* Primary MYSQL state struct definition */
struct st_mysql_options {
  unsigned int connect_timeout, read_timeout, write_timeout;
  unsigned int port, protocol;
  unsigned long client_flag;
  char *host,*user,*password,*unix_socket,*db;
  struct st_dynamic_array *init_commands;
  char *my_cnf_file,*my_cnf_group, *charset_dir, *charset_name;
  char *ssl_key;                /* PEM key file */
  char *ssl_cert;               /* PEM cert file */
  char *ssl_ca;                 /* PEM CA file */
  char *ssl_capath;             /* PEM directory of CA-s? */
  char *ssl_cipher;             /* cipher to use */
  char *shared_memory_base_name;
  unsigned long max_allowed_packet;
  my_bool use_ssl;              /* if to use SSL or not */
  my_bool compress,named_pipe;
  my_bool unused1;
  my_bool unused2;
  my_bool unused3;
  my_bool unused4;
  enum mysql_option methods_to_use;
  union {
    /*
      The ip/hostname to use when authenticating
      client against embedded server built with
      grant tables - only used in embedded server
    */
    char *client_ip;

    /*
      The local address to bind when connecting to
      remote server - not used in embedded server
    */
    char *bind_address;
  } ci;
  /* Refuse client connecting to server if it uses old (pre-4.1.1) protocol */
  my_bool secure_auth;
  /* 0 - never report, 1 - always report (default) */
  my_bool report_data_truncation;

  /* function pointers for local infile support */
  int (*local_infile_init)(void **, const char *, void *);
  int (*local_infile_read)(void *, char *, unsigned int);
  void (*local_infile_end)(void *);
  int (*local_infile_error)(void *, char *, unsigned int);
  void *local_infile_userdata;
  struct st_mysql_options_extention *extension;
};

struct st_mysql;
typedef struct st_mysql
{
  NET       net;            /* Communication parameters */
  unsigned char *connector_fd;      /* ConnectorFd for SSL */
  char      *host,*user,*passwd,*unix_socket,*server_version,*host_info;
  char          *info, *db;
  struct charset_info_st *charset;
  MYSQL_FIELD   *fields;
  MEM_ROOT  field_alloc;
  my_ulonglong affected_rows;
  my_ulonglong insert_id;       /* id if insert on table with NEXTNR */
  my_ulonglong extra_info;      /* Not used */
  unsigned long thread_id;      /* Id for connection in server */
  unsigned long packet_length;
  unsigned int  port;
  unsigned long client_flag,server_capabilities;
  unsigned int  protocol_version;
  unsigned int  field_count;
  unsigned int  server_status;
  unsigned int  server_language;
  unsigned int  warning_count;
  struct st_mysql_options options;
  enum mysql_status status;
  my_bool   free_me;        /* If free in mysql_close */
  my_bool   reconnect;      /* set to 1 if automatic reconnect */

  /* session-wide random string */
  char          scramble[21];
  my_bool unused1;
  void *unused2, *unused3, *unused4, *unused5;

  LIST  *stmts;                     /* list of all statements */
  const struct st_mysql_methods *methods;
  void *thd;
  /*
    Points to boolean flag in MYSQL_RES  or MYSQL_STMT. We set this flag 
    from mysql_stmt_close if close had to cancel result set of this object.
  */
  my_bool *unbuffered_fetch_owner;
  /* needed for embedded server - no net buffer to store the 'info' */
  char *info_buffer;
  void *extension;
} MYSQL;

/* Define the MYSQL_RES type */

typedef struct st_mysql_data {
  MYSQL_ROWS *data;
  struct embedded_query_result *embedded_info;
  MEM_ROOT alloc;
  my_ulonglong rows;
  unsigned int fields;
  /* extra info for embedded library */
  void *extension;
} MYSQL_DATA;

typedef struct st_mysql_res {
  my_ulonglong  row_count;
  MYSQL_FIELD   *fields;
  MYSQL_DATA    *data;
  MYSQL_ROWS    *data_cursor;
  unsigned long *lengths;       /* column lengths of current row */
  MYSQL     *handle;        /* for unbuffered reads */
  const struct st_mysql_methods *methods;
  MYSQL_ROW row;            /* If unbuffered read */
  MYSQL_ROW current_row;        /* buffer to current row */
  MEM_ROOT  field_alloc;
  unsigned int  field_count, current_field;
  my_bool   eof;            /* Used by mysql_fetch_row */
  /* mysql_stmt_close() had to cancel this result */
  my_bool       unbuffered_fetch_cancelled;  
  void *extension;
} MYSQL_RES;


/* Functions! */

MYSQL*   mysql_init(MYSQL *mysql);
MYSQL* mysql_real_connect(
    MYSQL *mysql, const char *host,
    const char *user,
    const char *passwd,
    const char *db,
    unsigned int port,
    const char *unix_socket,
    unsigned long clientflag);

char* mysql_error(MYSQL *mysql);
int mysql_real_query(MYSQL *mysql, char *q,
                    unsigned long length);
int mysql_query(MYSQL *mysql, char *q);
MYSQL_RES* mysql_store_result(MYSQL *mysql);
unsigned int mysql_num_fields(MYSQL_RES *res);
MYSQL_ROW mysql_fetch_row(MYSQL_RES *result);
unsigned long * mysql_fetch_lengths(MYSQL_RES *result);
MYSQL_FIELD * mysql_fetch_field(MYSQL_RES *result);
unsigned long mysql_escape_string(char *to,char *from,
                        unsigned long from_length);
unsigned long mysql_real_escape_string(MYSQL *mysql,
                           char *to,char *from,
                           unsigned long length);
my_ulonglong mysql_affected_rows(MYSQL *mysql);
char * mysql_get_server_info(MYSQL *mysql);
my_ulonglong mysql_insert_id(MYSQL *mysql);
my_bool mysql_autocommit(MYSQL * mysql, my_bool auto_mode);
my_bool mysql_commit(MYSQL * mysql);
my_bool mysql_rollback(MYSQL * mysql);

void mysql_free_result(MYSQL_RES *result);
char * mysql_character_set_name(MYSQL *mysql);
int mysql_options(MYSQL *mysql,enum mysql_option option,
                      void *arg);

/* RAW Access to sending a query. This is the key to ASYNC.

Anything that implicitly uses query wil call:
    mysql_send_query and mysql_read_query_result.

So we're going to explictly hijack those explicits
*/
int mysql_send_query(MYSQL *mysql, const char *q,
                     unsigned long length);
my_bool mysql_read_query_result(MYSQL *mysql);
unsigned int mysql_errno(MYSQL *mysql);
void mysql_close(MYSQL *sock);
    """)

# from ctypes verion:
# Hardcoded based on the values I found on two different Linux systems, bad: no
# cookies
MYSQL_OPT_CONNECT_TIMEOUT = 0
MYSQL_INIT_COMMAND = 3

c = ffi.dlopen('mysqlclient')
