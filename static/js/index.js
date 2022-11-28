Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-Я]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат имени нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },

            Costs: JSON.parse(JSON.parse(document.getElementById('costs').textContent)),
            Levels_data: JSON.parse(JSON.parse(document.getElementById('levels').textContent)),
            Form_data: JSON.parse(JSON.parse(document.getElementById('form').textContent)),
            Topping_data: JSON.parse(JSON.parse(document.getElementById('topping').textContent)),
            Berries_data: JSON.parse(JSON.parse(document.getElementById('berries').textContent)),
            Decor_data: JSON.parse(JSON.parse(document.getElementById('decor').textContent)),

            Costs_words: 500,
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: user_first_name,
            Phone: user_phonenumber,
            Email: user_email,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: ''
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs_words : 0
            
            levels = parseFloat(this.Costs[this.Levels]) || 0
            form = parseFloat(this.Costs[this.Form]) || 0
            topping = parseFloat(this.Costs[this.Topping]) || 0
            berries = parseFloat(this.Costs[this.Berries]) || 0
            decor = parseFloat(this.Costs[this.Decor]) || 0

            return levels + form + topping + berries + decor + W
        },
        Levels_computed() {
            return this.Levels_data[this.Levels]
        },
        Form_computed() {
            return this.Form_data[this.Form]
        },
        Topping_computed() {
            return this.Topping_data[this.Topping]
        },
        Berries_computed() {
            return this.Berries_data[this.Berries]
        },
        Decor_computed() {
            return this.Decor_data[this.Decor]
        },

    }
}).mount('#VueApp')