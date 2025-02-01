/** @odoo-module **/

import {SaleOrderLineProductField} from "@sale/js/sale_product_field";
import {patch} from "@web/core/utils/patch";

patch(SaleOrderLineProductField.prototype, {
    get extraLines() {
        var res = super.extraLines;
        if (
            this.props.record.data.is_contract &&
            this.props.record.data.product_contract_description
        ) {
            for (var val of this.props.record.data.product_contract_description.split(
                "||"
            )) {
                res.push(val);
            }
        }
        return res;
    },

    async _onProductUpdate() {
        super._onProductUpdate(...arguments);
        if (this.props.record.data.is_contract) {
            this._openContractConfigurator(true);
        }
    },

    _editLineConfiguration() {
        super._editLineConfiguration(...arguments);
        if (this.props.record.data.is_contract) {
            this._openContractConfigurator();
        }
    },

    get isConfigurableLine() {
        return super.isConfigurableLine || this.props.record.data.is_contract;
    },

    get contractContext() {
        return {
            default_product_id: this.props.record.data.product_id[0],
            default_partner_id: this.props.record.model.root.data.partner_id[0],
            default_company_id: this.props.record.model.root.data.company_id[0],
            default_product_uom_qty: this.props.record.data.product_uom_qty,
            default_contract_id: this.props.record.data.contract_id[0],
            default_recurring_interval: this.props.record.data.recurring_interval,
            default_date_start: this.props.record.data.date_start,
            default_date_end: this.props.record.data.date_end,
            default_is_auto_renew: this.props.record.data.is_auto_renew,
            default_auto_renew_interval: this.props.record.data.auto_renew_interval,
            default_auto_renew_rule_type: this.props.record.data.auto_renew_rule_type,
        };
    },

    async _openContractConfigurator(isNew = false) {
        const actionContext = this.contractContext;
        this.action.doAction("product_contract.product_contract_configurator_action", {
            additionalContext: actionContext,
            onClose: async (closeInfo) => {
                if (closeInfo && !closeInfo.special) {
                    this.props.record._update(closeInfo.productContractConfiguration, {
                        withoutOnchange: true,
                    });
                } else if (isNew) {
                    this.props.record.update({
                        [this.props.name]: undefined,
                    });
                }
            },
        });
    },
});
