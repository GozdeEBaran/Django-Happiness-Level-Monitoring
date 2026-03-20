from django.urls import reverse
from drf_spectacular.openapi import AutoSchema as Schema
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.authentication import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import warn, ResolvedComponent
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AutoSchema(Schema):
    # Drf spectacular does not recognize jwt authentication token
    # if authenticator is set to [], and it does not sent in header.
    # Therefore needs to be overridden for swagger views
    def get_auth(self):
        auths = []
        authenticators = self.view.get_authenticators()
        if self.path == reverse('happiness-stats-list'):
            authenticators = [JWTAuthentication]

        for authenticator in authenticators:
            if (
                spectacular_settings.AUTHENTICATION_WHITELIST
                and authenticator.__class__ not in spectacular_settings.AUTHENTICATION_WHITELIST
            ):
                continue

            scheme = OpenApiAuthenticationExtension.get_match(authenticator)
            if not scheme:
                warn(
                    f'could not resolve authenticator {authenticator.__class__}. There '
                    f'was no OpenApiAuthenticationExtension registered for that class. '
                    f'Try creating one by subclassing it. Ignoring for now.'
                )
                continue

            security_requirements = scheme.get_security_requirement(self)
            if security_requirements is not None:
                auths.append(security_requirements)

            component = ResolvedComponent(
                name=scheme.name,
                type=ResolvedComponent.SECURITY_SCHEMA,
                object=authenticator.__class__,
                schema=scheme.get_security_definition(self)
            )
            self.registry.register_on_missing(component)

        if spectacular_settings.SECURITY:
            auths.extend(spectacular_settings.SECURITY)

        perms = [p.__class__ for p in self.view.get_permissions()]
        if permissions.AllowAny in perms:
            auths.append({})
        elif permissions.IsAuthenticatedOrReadOnly in perms and self.method in permissions.SAFE_METHODS:
            auths.append({})
        return auths
