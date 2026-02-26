from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ReviewViewSet, RatingViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls