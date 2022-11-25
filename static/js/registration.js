Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                reg: (value) => {
                    if (value) {
                        return true;
                    }
                    return 'Поле не заполнено';
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                code_format: (value) => {
                    const regex = /^[a-zA-Z0-9]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат кода нарушен';
                    }
                    return true;
                }
            },
            Step: 'Number',
            RegInput: '',
            EnteredNumber: ''
        }
    },
    methods: {
        RegSubmit() {
            if (this.Step === 'Number') {
                var formData = new FormData();
                var error = false;
                formData.append('phone_number', this.RegInput);
                $.ajax({
                    type: 'POST',
                    url: 'register/',
                    headers: { 'X-CSRFToken': CSRF_TOKEN },
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response){
					if (response.phone_number_error)
					    {
                     	alert(response.phone_number_error);
                     	window.location.reload();
                     	}
					}
                });
                this.Step = 'Code';
                this.EnteredNumber = this.RegInput;
                this.RegInput = '';
            }
            else {
                this.$refs.HiddenFormSubmitReg.click()
                this.Step = 'Finish'
                this.RegInput = 'Регистрация успешна'
            }
        },
        ToRegStep1() {
            this.Step = 'Number'
            this.RegInput = this.EnteredNumber
        },
        Reset() {
            this.Step = 'Number'
            this.RegInput = ''
            EnteredNumber = ''
        }
    }
}).mount('#RegModal')