const { ref, onMounted, computed } = Vue

const Home = {
    setup() {
        const query = ref('O que é NOMA?')
        const chunks = ref('')
        const prompt = ref({
            Prompt: '',
            System_Prompt: '',
            Prompt_Expansao: ''
        })

        const processedPrompt = computed(() => {
            if (!prompt.value) return ''
            return prompt.value.Prompt
                .replace('{query}', query.value || '{query}')
                .replace('{chunks}', chunks.value || '{chunks}')
        })

        const loadPromptTemplate = async () => {
            try {
                const response = await fetch('/api/get_prompt')
                const getChunks = await fetch(`/api/fetch_chunks?search=${encodeURIComponent(query.value)}`)

                const chunkss = await getChunks.json()
                const data = await response.json()
                
                prompt.value = data || 'No prompt available'
                chunks.value = chunkss.chunks || 'No chunks available'

                console.log('Loaded prompt:', prompt.value)
            } catch (error) {
                console.error('Error loading prompt template:', error)
            }
        }

        const search = async () => {
            try {
                const getChunks = await fetch(`/api/fetch_chunks?search=${encodeURIComponent(query.value)}`)
                const chunkss = await getChunks.json()

                chunks.value = chunkss.chunks
            } catch (error) {
                console.error('Error fetching chunks:', error)
            }
        }

        onMounted(() => {
            loadPromptTemplate()
        })
        
        return {
            query,
            prompt,
            processedPrompt,
            search
        }
    },
    template: `
        <div class="container mx-auto px-4 py-8">
            <div class="grid grid-cols-2 gap-4">
                <!-- Left Column -->
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="text-xl font-bold mb-4">Search</h2>
                    <input 
                        type="text" 
                        v-model="query" 
                        class="border p-2 rounded w-full"
                        placeholder="Search..."
                    >

                    <button type="button" @click="search" class="bg-blue-500 text-white px-4 py-2 rounded mt-2">Search</button>
                </div>

                <!-- Middle Column -->
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="text-xl font-bold mb-4">Prompt Template</h2>
                    <p class="whitespace-pre-wrap bg-gray-100 p-4 rounded">
                        {{ prompt.System_Prompt }}
                    </p>

                    <p class="whitespace-pre-wrap bg-gray-100 p-4 rounded">
                        {{ processedPrompt }}
                    </p>
                </div>

                <!-- Right Column
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="text-xl font-bold mb-4">Details</h2>
                    <div v-if="prompt">
                        <p class="mb-2">Template loaded successfully</p>
                    </div>
                </div>
                -->
            </div>
        </div>
    `
}