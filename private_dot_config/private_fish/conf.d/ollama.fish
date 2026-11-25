# Ollama Vulkan iGPU + 128K Context Configuration
# Managed via chezmoi

set -gx OLLAMA_IGPU_ENABLE 1
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0
set -gx OLLAMA_CONTEXT_LENGTH 131072
