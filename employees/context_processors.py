from .models import Organization


def organization_context(request):
    """
    Context processor to make organization information available in all templates
    """
    try:
        # Get the first active organization (assuming single organization setup)
        organization = Organization.objects.filter(is_active=True).first()

        if organization:
            return {
                'organization': organization,
                'company': organization,  # Backward compatibility
                'company_name': organization.display_name,
                'organization_name': organization.display_name,
                'organization_type': organization.get_organization_type_display(),
                'organization_hierarchy': organization.organization_hierarchy,
                'company_address': organization.full_address,
                'organization_address': organization.full_address,
                'company_phone': organization.phone_number,
                'organization_phone': organization.phone_number,
                'company_email': organization.email,
                'organization_email': organization.email,
                'company_kra_pin': organization.kra_pin,
                'organization_kra_pin': organization.kra_pin,
                'ministry': organization.ministry,
                'sector': organization.sector,
            }
        else:
            # Default values if no organization is configured
            return {
                'organization': None,
                'company': None,
                'company_name': 'Your Organization Name',
                'organization_name': 'Your Organization Name',
                'organization_type': 'Organization',
                'organization_hierarchy': 'Your Organization Name',
                'company_address': 'Organization Address',
                'organization_address': 'Organization Address',
                'company_phone': '+254 XXX XXX XXX',
                'organization_phone': '+254 XXX XXX XXX',
                'company_email': 'info@organization.go.ke',
                'organization_email': 'info@organization.go.ke',
                'company_kra_pin': 'PXXXXXXXXX',
                'organization_kra_pin': 'PXXXXXXXXX',
                'ministry': '',
                'sector': '',
            }
    except Exception:
        # Fallback in case of database issues
        return {
            'organization': None,
            'company': None,
            'company_name': 'Your Organization Name',
            'organization_name': 'Your Organization Name',
            'organization_type': 'Organization',
            'organization_hierarchy': 'Your Organization Name',
            'company_address': 'Organization Address',
            'organization_address': 'Organization Address',
            'company_phone': '+254 XXX XXX XXX',
            'organization_phone': '+254 XXX XXX XXX',
            'company_email': 'info@organization.go.ke',
            'organization_email': 'info@organization.go.ke',
            'company_kra_pin': 'PXXXXXXXXX',
            'organization_kra_pin': 'PXXXXXXXXX',
            'ministry': '',
            'sector': '',
        }
