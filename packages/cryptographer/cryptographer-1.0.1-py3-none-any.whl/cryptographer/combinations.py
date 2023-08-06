def combine_ciphers(name, ciphers):
    cipher_names = [cipher.__name__.lower() for cipher in ciphers]
    for i in range(len(cipher_names)):
        cipher_name = cipher_names[i]
        if cipher_name.lower().endswith('key'):
            cipher_name = cipher_name[:-3]
        cipher_names[i] = cipher_name

    def __init__(self, **kwargs) -> None:
        self._name = name
        self.ciphers = ciphers
        self.cipher_names = cipher_names

        for key, value in kwargs.items():
            if key.lower() in self.cipher_names:
                setattr(self, f'_{key}_cipher', value)
        
        for cipher_name in self.cipher_names:
            if not hasattr(self, f'{cipher_name}_cipher'):
                setattr(self, f'_{cipher_name}_cipher', None)
    
    def __getstate__(self) -> dict:
        """Prepare self for pickling."""
        state = {
            'ciphers': self.ciphers,
            'cipher_names': self.cipher_names,
        }
        for cipher_name in self.cipher_names:
            state[f'_{cipher_name}_cipher'] = getattr(self, f'_{cipher_name}_cipher')
        
        return state
    
    def __setstate__(self, data) -> None:
        """Prepare self for unpickling."""
        for key, value in data.items():
            setattr(self, key, value)
    
    def __repr__(self):
        """return repr(self)"""
        return f'<{self._name}_CombinedCipher>'
    
    __str__ = __repr__
    __str__.__doc__ = """return str(self)"""

    def encrypt(self, data) -> (str, bytes):
        """encrypt data"""
        for cipher_name in self.cipher_names:
            if getattr(self, f'_{cipher_name}_cipher') != None:
                data = getattr(self, f'_{cipher_name}_cipher').encrypt(data)
        return data
    
    def decrypt(self, data) -> (str, bytes):
        """decrypt data"""
        for cipher_name in self.cipher_names[::-1]:
            if getattr(self, f'_{cipher_name}_cipher') != None:
                data = getattr(self, f'_{cipher_name}_cipher').decrypt(data)
        return data
    
    def get_key(self, key) -> any:
        """return self's key"""
        return getattr(self, f'_{key}_cipher')
    
    def set_key(self, key, value) -> None:
        """set self's key"""
        setattr(self, f'_{key}_cipher', value)
    
    __doc__ = f"""
"{name}" Combined Cipher
"""
    
    cls = type(
        name,
        (),
        {
            '__init__': __init__,
            '__getstate__': __getstate__,
            '__setstate__': __setstate__,
            '__doc__': __doc__,
            '__repr__': __repr__,
            '__str__': __str__,
            'encrypt': encrypt,
            'decrypt': decrypt,
            'get_key': get_key,
            'set_key': set_key,
            '__module__': 'builtins',
        }
    )

    return cls