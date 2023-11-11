<template>
    <div class="px-6 col-span-2 flex flex-col pt-4 border-r-[1px] border-gray-200">
      <div>
        <button
          class="flex items-center text-center bg-gray-light px-10 py-1 rounded-xl font-bold mb-3"
        >
          Select LLM
        </button>
      </div>

      <p class="mb-3"><span class="font-medium">ChatGPT</span> loaded.</p>
      <div class="bg-gray-light grow flex flex-col px-3 rounded-xl justify-end py-3 min-h-[1px] shadow-sm">
        <div class="flex items-center">
        <div
          class="bg-gray-dark w-full h-8 rounded-xl px-2 text-sm font-semibold flex items-center place-self-end"
        >
          Enter a Prompt...
        </div>

        </div>
      </div>
    </div>
</template>