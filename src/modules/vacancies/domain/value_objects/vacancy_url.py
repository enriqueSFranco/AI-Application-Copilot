from urllib.parse import urlparse

import validators


class InvalidUrlError(ValueError):
    """Excepción personalizada para URLs inválidas."""

    pass


class VacancyUrl:
    def __init__(self, url: str):
        if not url:
            raise InvalidUrlError("La URL no puede estar vacía.")
        if not validators.url(url):
            raise InvalidUrlError(f"La cadena '{url}' no es una URL válida.")

        parsed_url = urlparse(url)
        self._value = parsed_url.geturl() if parsed_url.scheme else f"http://{url}"

    def _get_site_name(self, url: str):
        """Obtiene el nombre del stio web a partir de una URL.

        Intenta devolver solo la parte inicial del dominio,
        eliminando subdominios como "www" y manejando TDL compuestos
        como ".com.mx".

        Args:
            url (str): La URL a analizar.

        Returns:
            str: Nombre principal del sitio (por ejemplo, 'linkedin', 'occ', 'glassdoor').
        """
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname or ""
        # Eliminar el prefijo "www." si existe
        hostname = hostname.removeprefix("www.")

        parts = hostname.split(".")

        if len(parts) >= 3 and parts[-1] == "mx":
            return parts[-3]

        if len(parts) >= 2:
            return parts[-2]
        return hostname

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"JobUrl(url='{self._value}', site_name='{self.site_name}')"

    def __eq__(self, other: object):
        if isinstance(other, JobUrl):
            return self._value == other._value
        return False

    def __hash__(self):
        return hash(self._value)

    @property
    def value(self):
        return self._value

    @property
    def site_name(self):
        return self._get_site_name(self._value)
