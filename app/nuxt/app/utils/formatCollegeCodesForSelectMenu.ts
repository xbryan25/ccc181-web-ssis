import type { SelectMenuItem } from "@nuxt/ui"

import type { UseCollegeCodesResponse } from "~/types";

export function formatCollegeCodesForSelectMenu(collegeCodesDetails: UseCollegeCodesResponse[]): SelectMenuItem[] {
	const collegeCodesDetailsFormatted: SelectMenuItem[] = []
	
	for (const i in collegeCodesDetails) {
		collegeCodesDetailsFormatted.push({ label: collegeCodesDetails[i]?.collegeCode });
	}

	console.log(collegeCodesDetails)

	return collegeCodesDetailsFormatted
}
