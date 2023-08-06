from typing import Dict
from django.urls import re_path, include, path

from rest_framework.routers import DefaultRouter, format_suffix_patterns, APIRootView as Arw
from rest_framework.viewsets import ViewSetMixin


__all__ = [
    "APIRouter",
]


class APIRootView(Arw):
    """API root."""


class APIRouter(DefaultRouter):
    """Router that will show APIViews in API root."""

    root_view_name = "api-root"
    APIRootView = APIRootView
    
    navigation_routes: Dict[str, "DefaultRouter"] = {}
    """Add urls from these routers to this routers urls under the root-view of the added router, 
    which will be named after the given key. This enables browser navigation of the API."""

    def format_root_view(self, name: str, docsctring: str):
        """Format the root view browsable API documentation.

        :param name: Root display name. CamelCase or snake_case to separate words.
        :param docsctring: Used as view documentation.
        """
        new_root: APIRootView = type(name, (APIRootView,), {})  # noqa
        new_root.__doc__ = docsctring
        self.APIRootView = new_root

    def get_routes(self, viewset):
        if issubclass(viewset, ViewSetMixin):
            return super().get_routes(viewset)
        return []

    def get_api_root_view(self, api_urls=None):
        api_root_dict = {}
        list_name = self.routes[0].name

        for prefix, viewset, basename in self.registry:
            if issubclass(viewset, ViewSetMixin):
                api_root_dict[prefix] = list_name.format(basename=basename)
            else:
                api_root_dict[prefix] = basename

        for basename in self.navigation_routes:
            api_root_dict[fr"{basename}"] = basename

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def get_urls(self):
        urls = []
        for prefix, viewset, basename in self.registry:
            if issubclass(viewset, ViewSetMixin):
                continue

            regex = r"^{prefix}{trailing_slash}$".format(prefix=prefix, trailing_slash=self.trailing_slash)

            urls.append(re_path(regex, viewset.as_view(), name=basename))

        urls = format_suffix_patterns(urls)

        for basename, router in self.navigation_routes.items():
            router.root_view_name = basename
            urls.append(path(f"{basename}/", include(router.urls)))

        return super().get_urls() + urls

