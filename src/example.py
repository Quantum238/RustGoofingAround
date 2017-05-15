import cffi



def get_string_from_void_ptr(ptr, must_cast = False):
	NULL = b'\x00'
	if must_cast:
		ptr = ffi.cast('char *', ptr)
	bytes_ = b''
	idx = 0
	while True:
		char_ = ptr[idx]
		if char_ == NULL:
			break
		else:
			bytes_ += char_
			idx += 1
	lib.theme_song_free(ptr)
	return bytes_.decode('utf8')

ffi = cffi.FFI()
lib = ffi.dlopen('../target/debug/libdannyexample.so')

ffi.cdef("""
	int addition(int, int);

	int how_many_characters(char[]);

	void * theme_song_generate(int);
	void theme_song_free(void *);

	int sum_of_even(int *, int);

	typedef struct {
		int x;
		int y;
	} tuple_t;
	tuple_t flip_things_around( tuple_t );

	void * zip_code_database_new();
	void zip_code_database_free(void *);
	void zip_code_database_populate(void *);
	int zip_code_database_population_of(void *, char[]);

	""")
print(lib.addition(1, 2))
print(lib.how_many_characters(b"hello"))
print(get_string_from_void_ptr(lib.theme_song_generate(12), True))
numbers = [1, 2, 3, 4, 5, 6]
ptr_to_numbers = ffi.new('int[]', numbers)
print(lib.sum_of_even(ptr_to_numbers, len(ptr_to_numbers)))

tuple_ptr = ffi.new('tuple_t *', [7,9])
tuple_ = tuple_ptr[0]
print(tuple_.x, tuple_.y)
res = lib.flip_things_around(tuple_)
print(res.x, res.y)

zip_db_ptr = lib.zip_code_database_new()
lib.zip_code_database_populate(zip_db_ptr)
print(lib.zip_code_database_population_of(zip_db_ptr, b'90210'))
print(lib.zip_code_database_population_of(zip_db_ptr, b'20500'))
lib.zip_code_database_free(zip_db_ptr)
