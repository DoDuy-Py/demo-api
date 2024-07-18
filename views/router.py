from fastapi import APIRouter
from .water_quality import WaterQualityView
from .auth import Authentication
from .user_views import UserViewSet, RoleViewSet


router = APIRouter()

# Tạo một instance của WaterQualityView và đăng ký router
water_quality_view = WaterQualityView()
router.add_api_route("/create-water/", water_quality_view.create, methods=["POST"])
router.add_api_route("/get-water/", water_quality_view.get, methods=["GET"])
router.add_api_route("/water-quality/{id}", water_quality_view.detail, methods=["GET"])
router.add_api_route("/water-quality/{id}", water_quality_view.update, methods=["PUT"])
router.add_api_route("/water-quality/{id}", water_quality_view.remove, methods=["DELETE"])

# AUTH
auth = Authentication()
router.add_api_route("/sign-in/", auth.login_access_token, methods=["POST"])
router.add_api_route("/sign-up/", auth.signup, methods=["POST"])

user_views = UserViewSet()
router.add_api_route("/profile/{id}/", user_views.get_profile, methods=["GET"])
router.add_api_route("/create-user/", user_views.create, methods=["POST"])

user_role = RoleViewSet()
router.add_api_route("/update-roles-user/", user_role.update_roles_user, methods=["POST"])