# Django Browsable Router
A Django Restframework router that can show APIViews and include other routers as navigable urls in the root view.

```python
class TestView(APIView):
  ...
 
class TestViewSet(ViewSet):
  ...

router_1 = APIRouter()
router_1.format_root_view("other_routes", "These are under a different route.")
router_1.register(r"view-1", TestView.as_view(), "view_1")
router_1.register(r"view-2", TestViewSet.as_view(), "view_2")

router_2 = APIRouter()
router_2.register(r"view-3", TestView.as_view(), "view_3")
router_2.navigation_routes = {
    "route": router_1,
}

urlpatterns = [
    path("api/", include(router_2.urls))
]


#   API Root:
#   """API root."""
# 
#   "route":    "/api/route/"
#   "view-3":   "/api/view-3/"
# 
#   Other Routes:
#   """These are under a different route."""
# 
#   "view-1":    "/api/route/view-1/"
#   "view-2":    "/api/route/view-2/"

```
