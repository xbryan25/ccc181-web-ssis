<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <div>
    <div class="flex flex-col gap-10 h-full">
      <h1 class="font-bold text-5xl">About</h1>
      <div class="flex flex-col items-center gap-4 px-[20%]">
        <USeparator color="primary" type="solid">
          <h2 class="font-bold text-4xl">What is Sequence?</h2>
        </USeparator>

        <div class="flex flex-col items-center gap-4">
          <p class="text-md text-justify w-full">
            Sequence is a web-based simple student information system (SSIS) made in accordance with
            the requirements of CCC181. The name 'Sequence' reflects how the web application
            organizes data in a defined order.
          </p>

          <p class="text-md text-justify w-full">
            This web application supports the create, read, update, delete, and list (CRUDL)
            operations for students, programs, and colleges. Records can also be sorted and searched
            according to a criteria that will be set by the users. This web application also
            supports basic user authentication.
          </p>

          <p class="text-md text-justify w-full">
            This full-stack web application massively improves upon the
            <a
              href="https://github.com/xbryan25/ccc151-ssis-v2"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-block underline transition-transform duration-300 hover:scale-102"
            >
              desktop version of the SSIS
            </a>

            created in the previous semester.
          </p>
        </div>
      </div>
      <div class="flex flex-col items-center gap-8 px-[20%]">
        <USeparator color="primary" type="solid">
          <h2 class="font-bold text-4xl">Tech Stack</h2>
        </USeparator>
        <div class="flex flex-col gap-4 w-full">
          <div class="flex flex-col items-center gap-5 w-full">
            <h2 class="font-bold text-2xl">Frontend</h2>
            <div class="flex justify-center w-full max-w-125 overflow-hidden mx-auto">
              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Vue"
                :ui="{ content: 'py-5 bg-neutral', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:vuejs" class="size-25 shrink-0" />
              </UTooltip>

              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Nuxt"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:nuxt" class="size-25 shrink-0" />
              </UTooltip>

              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="TailwindCSS"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:tailwindcss" class="size-25 shrink-0" />
              </UTooltip>
            </div>
          </div>
          <div class="flex flex-col items-center gap-5 w-full">
            <h2 class="font-bold text-2xl">Backend</h2>
            <div class="flex justify-center w-full max-w-125 overflow-hidden mx-auto">
              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Flask"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="skill-icons:flask-light" class="size-25 shrink-0" />
              </UTooltip>

              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Python"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:python" class="size-25 shrink-0" />
              </UTooltip>
            </div>
          </div>
          <div class="flex flex-col items-center gap-5 w-full">
            <h2 class="font-bold text-2xl">Database</h2>
            <div class="flex justify-center w-full max-w-125 overflow-hidden mx-auto">
              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="PostgreSQL"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:postgresql" class="size-25 shrink-0" />
              </UTooltip>
            </div>
          </div>
          <div class="flex flex-col items-center gap-5 w-full">
            <h2 class="font-bold text-2xl">Tools</h2>
            <div class="flex justify-center w-full max-w-125 overflow-hidden mx-auto">
              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Docker"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:docker" class="size-25 shrink-0" />
              </UTooltip>

              <UTooltip
                :content="{
                  align: 'center',
                  side: 'top',
                  sideOffset: 4,
                }"
                text="Postman"
                :ui="{ content: 'py-5', text: 'text-xl text-neutral' }"
                class="flex-1"
              >
                <UIcon name="devicon:postman" class="size-25 shrink-0" />
              </UTooltip>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-center h-20 pt-10">
      <p class="text-primary">
        Made with love by
        <a
          href="https://github.com/xbryan25"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-block underline transition-transform duration-300 hover:scale-105"
        >
          @xbryan25
        </a>
      </p>
    </div>
  </div>
</template>
