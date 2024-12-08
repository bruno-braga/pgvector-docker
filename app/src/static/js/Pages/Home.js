const { ref, onMounted, onBeforeUnmount, computed, defineProps } = Vue

const Home = {
    setup() {
        const messages = ref([])
        const query = ref('O que é NOMA?')
        const answer = ref(null)
        const typedInstances = ref({})
        const isLoading = ref(false)

        const search = async () => {
            isLoading.value = true
            try {
                const response = await fetch(`/rag/search/${encodeURIComponent(query.value)}`)
                const data = await response.json()

                console.log(data)

                const newMessage = {
                    question: query.value,
                    answer: data.response,
                    id: Date.now()
                }

                messages.value.push(newMessage)

                query.value = ''

                await Vue.nextTick()

                const latestAnswerElement = document.querySelector(`#answer-${newMessage.id}`)
                typedInstances.value[newMessage.id] = new Typed(latestAnswerElement, {
                    strings: [data.response],
                    typeSpeed: 10,
                    cursor: '|'
                })

                return data
            } finally {
                isLoading.value = false
            }
        }

        const handleSubmit = async (e) => {
            e.preventDefault()
            if (query.value.trim()) {
                await search()
            }
        }

        onMounted(async () => {
            await search()
        })

        onBeforeUnmount(() => {
            Object.values(typedInstances.value).forEach(instance => {
                if (instance) {
                    instance.destroy()
                }
            })
        })

        return {
            answer,
            query,
            search,
            messages,
            handleSubmit,
            isLoading
        }
    },
    template: /* html */ ` 
        <div class="container mx-auto px-4 py-8 max-w-screen-md h-screen flex flex-col">
            <div class="flex-1 overflow-y-auto mb-24">
                <div class="space-y-4">
                    <div v-for="message in messages" :key="message.id" class="bg-white p-4 rounded shadow">
                        <div class="font-semibold mb-2">{{ message.question }}</div>
                        <span :id="'answer-' + message.id"></span>
                    </div>
                </div>
            </div>

            <div class="bg-white p-4 rounded shadow fixed bottom-0 left-1/2 -translate-x-1/2 mb-4 max-w-4xl w-[calc(100%-2rem)]">
                <form @submit="handleSubmit" class="flex">
                    <input 
                        type="text" 
                        v-model="query" 
                        class="border p-2 rounded w-full"
                        placeholder="Ask something... please! :-)"
                    >

                    <button 
                        type="submit" 
                        class="bg-blue-500 text-white px-4 py-2 rounded ml-2 flex items-center" 
                        :disabled="isLoading"
                    >
                        <svg 
                            v-if="isLoading"
                            class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" 
                            xmlns="http://www.w3.org/2000/svg" 
                            fill="none" 
                            viewBox="0 0 24 24"
                        >
                            <circle 
                                class="opacity-25" 
                                cx="12" 
                                cy="12" 
                                r="10" 
                                stroke="currentColor" 
                                stroke-width="4"
                            ></circle>
                            <path 
                                class="opacity-75" 
                                fill="currentColor" 
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            ></path>
                        </svg>
                        {{ isLoading ? 'Thinking...' : 'Ask' }}
                    </button>
                </form>
            </div>
        </div>
    `
}