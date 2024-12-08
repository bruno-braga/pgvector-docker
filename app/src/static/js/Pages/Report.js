const { usePage } = InertiaVue

const Loader = {
    props: {
        text: {
            type: String,
            default: 'Loading...'
        }
    },
    template: /* html */ `
        <div class="flex justify-center items-center py-4 gap-3">
            <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-blue-500 text-lg">{{ text }}</span>
        </div>
    `
}

const Report = {
    components: {
        Loader
    },
    setup() {
        const messages = ref([])
        const query = ref('O que é NOMA?')
        const answer = ref(null)
        const typedInstances = ref({})
        const isLoading = ref(false)

        const page = usePage()
        const selectedTitle = ref(null)
        const titles = computed(() => page.props.value.titles)

        const chunks = ref([])
        const isChunksLoading = ref(false)

        const referenceAnswer = ref('')
        const isReferenceLoading = ref(false)

        const evaluation = ref('')
        const isEvaluationLoading = ref(false)

        const getChunks = async () => {
            const response = await fetch(`/rag/get_chunks/${query.value}`)
            const data = await response.json()
            return data.chunks
        }

        const getReferenceAnswer = async () => {
            const response = await fetch(`/rag/get_reference/${query.value}`)
            const data = await response.json()
            return data.reference_answer
        }

        const postData = async (url, data) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            return await response.json();
        }

        const handleSubmit = async (e) => {
            e.preventDefault()

            isChunksLoading.value = true
            const chunkss = await getChunks()
            chunks.value = chunkss
            isChunksLoading.value = false

            const textChunks = chunkss.map(chunk => chunk.text)

            isReferenceLoading.value = true
            const response = await getReferenceAnswer()
            referenceAnswer.value = response
            isReferenceLoading.value = false

            isEvaluationLoading.value = true
            const evaluationResponse = await postData('/rag/evaluate', {
                query: query.value,
                chunks: textChunks,
                reference: referenceAnswer.value
            })
            console.log('Evaluation Response:', evaluationResponse)
            evaluation.value = typeof evaluationResponse === 'string' 
                ? JSON.parse(evaluationResponse) 
                : evaluationResponse
            isEvaluationLoading.value = false

            console.log(evaluation)


            // if (query.value.trim()) {
            //     await search()
            // }
        }

        return {
            messages,
            query,
            answer,
            typedInstances,
            isLoading,
            titles,
            selectedTitle,
            handleSubmit,

            isChunksLoading,
            chunks,

            isReferenceLoading,
            referenceAnswer,

            isEvaluationLoading,
            evaluation
        }
    },
    template: /* html */ ` 
        <div class="container mx-auto px-4 py-8 max-w-screen-md h-screen flex flex-col">
            <div class="flex-1 overflow-y-auto mb-24 max-h-[400px]">
                <Loader v-if="isChunksLoading" text="Loading chunks..." />
                <div v-else class="space-y-4">
                    <div v-for="chunk in chunks" :key="chunk.id" class="bg-white p-4 rounded shadow">
                        <div class="font-semibold mb-2">{{ chunk.text }}</div>
                        <span :id="'answer-' + chunk.id"></span>
                    </div>
                </div>
            </div>

            <div class="mb-24">
                <Loader v-if="isReferenceLoading" text="Loading reference answer..." />
                <div v-else class="space-y-4">
                    <div class="font-semibold mb-2" v-if="referenceAnswer !== ''">Reference Answer:</div>
                    <div v-if="referenceAnswer !== ''">{{ referenceAnswer }}</div>
                </div>
            </div>

            <div class="mb-24">
                <Loader v-if="isEvaluationLoading" text="Evaluating... this might take a while." />
                <div v-else-if="evaluation && evaluation.results" class="space-y-4">
                    <div class="font-semibold mb-2">Evaluation:</div>
                    <div class="space-y-2">
                        <div v-for="(value, key) in evaluation.results" :key="key" class="bg-gray-50 p-4 rounded">
                            <span class="font-medium">{{ key.replace('_', ' ').charAt(0).toUpperCase() + key.slice(1) }}:</span>
                            <span class="ml-2">{{ value[0] }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-white p-4 rounded shadow fixed bottom-0 mb-[100px] left-1/2 -translate-x-1/2 mb-4 max-w-4xl w-[calc(100%-2rem)]">
                <form class="flex w-full">
                    <select
                        v-model="selectedTitle"
                        class="border p-2 rounded w-full"
                    >
                        <option v-for="title in titles" :value="title">{{ title }}</option>
                    </select>
                </form>
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
                        {{ isLoading ? 'Thinking...' : 'Evaluate' }}
                    </button>
                </form>
            </div>
        </div>
    `
}