from rest_framework import serializers

from nautobot.core.api import WritableNestedSerializer
from nautobot.tenancy.models import Tenant, TenantGroup

__all__ = [
    "NestedTenantGroupSerializer",
    "NestedTenantSerializer",
]


#
# Tenants
#


class NestedTenantGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="tenancy-api:tenantgroup-detail")
    tenant_count = serializers.IntegerField(read_only=True)
    _depth = serializers.IntegerField(source="level", read_only=True)

    class Meta:
        model = TenantGroup
        fields = ["id", "url", "name", "slug", "tenant_count", "_depth"]


class NestedTenantSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="tenancy-api:tenant-detail")

    class Meta:
        model = Tenant
        fields = ["id", "url", "name", "slug"]
