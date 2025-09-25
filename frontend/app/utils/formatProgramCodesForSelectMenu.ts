import type { SelectMenuItem } from "@nuxt/ui"

import type { UseProgramCodesResponse } from "~/types";

export function formatProgramCodesForSelectMenu(programCodesDetails: UseProgramCodesResponse[]): SelectMenuItem[] {
	const programCodesDetailsFormatted: SelectMenuItem[] = []
	
	for (let i = 0; i < programCodesDetails.length; i++) {

		if (i != 0){
			programCodesDetailsFormatted.push({type: 'separator' as const})
		}

		programCodesDetailsFormatted.push({type: 'label' as const, label: programCodesDetails[i]?.collegeCode})

		for (const programCode of programCodesDetails[i]?.programCodes ?? []) {
			programCodesDetailsFormatted.push({ label: programCode });
		}
	}

	return programCodesDetailsFormatted
}

// Reference
//
// const programCodeOptions = ref<SelectMenuItem[]>([
//   {
//     type: 'label',
//     label: 'CCS',
//   },
//   {
//     label: 'BSCS',
//   },
//   {
//     label: 'BSCA',
//   },
//   {
//     label: 'BSIS',
//   },
//   {
//     label: 'BSIT',
//   },
//   {
//     type: 'separator',
//   },
//   {
//     type: 'label',
//     label: 'COE',
//   },
//   {
//     label: 'BSCE',
//   },
// ]);