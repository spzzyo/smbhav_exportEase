from django import forms

class ImportChargesForm(forms.Form):
    product_value = forms.FloatField(
        label="Product Value (EUR)", 
        required=True,
        help_text="Enter the value of the furniture in EUR."
    )
    shipping_cost = forms.FloatField(
        label="Shipping Cost (EUR)", 
        required=True,
        help_text="Enter the shipping cost in EUR."
    )
    insurance_cost = forms.FloatField(
        label="Insurance Cost (EUR)", 
        required=True,
        help_text="Enter the insurance cost in EUR."
    )

    # Optional fields for users who may want to override default rates
    import_duty_rate = forms.FloatField(
        label="Import Duty Rate (%)", 
        required=False, 
        initial=25.0,
        help_text="Default rate for furniture imports is 25%."
    )
    tax_rate = forms.FloatField(
        label="IGST Rate (%)", 
        required=False, 
        initial=18.0,
        help_text="Default IGST rate for furniture imports is 18%."
    )
