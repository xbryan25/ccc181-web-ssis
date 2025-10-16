import type { FormError} from '@nuxt/ui';
import type { StudentFormState, ProgramFormState, CollegeFormState } from '~/types';

function isStudent(state: StudentFormState | ProgramFormState | CollegeFormState, entityType: string): state is StudentFormState {
  return entityType === 'student'
}

function isProgram(state: StudentFormState | ProgramFormState | CollegeFormState, entityType: string): state is ProgramFormState {
  return entityType === 'program'
}

function isCollege(state: StudentFormState | ProgramFormState | CollegeFormState, entityType: string): state is CollegeFormState {
  return entityType === 'college'
}

export function validateForm (state: StudentFormState | ProgramFormState | CollegeFormState, entityType: string, hasCalled: boolean): FormError[] {

	const idNumberRegex = /^\d{4}-\d{4}$/;
	const nameRegex = /^[A-Za-z- ]+$/;

	const programCodeRegex = /^[A-Z-]+$/;
	const programNameRegex = /^[A-Za-z- ]+$/;

  const collegeCodeRegex = /^[A-Z-]+$/;
  const collegeNameRegex = /^[A-Za-z- ]+$/;

	const whitespaceRegex = /^\s*$/;

  const errors: { name: string, message: string }[] = [];

	if (!hasCalled) return errors;

	if (isStudent(state, entityType)){
		if (!state.idNumber || whitespaceRegex.test(state.idNumber)) {
			errors.push({ name: 'idNumber', message: 'Required.' });
		} else if (state.idNumber && !idNumberRegex.test(state.idNumber)) {
			errors.push({
				name: 'idNumber',
				message: 'ID number format is XXXX-XXXX.',
			});
		}

		if (!state.firstName || whitespaceRegex.test(state.firstName)) {
			errors.push({ name: 'firstName', message: 'Required.' });
		} else if (state.firstName && !nameRegex.test(state.firstName)) {
			errors.push({
				name: 'firstName',
				message: 'Letters, spaces, and dashes only.',
			});
		}

		if (!state.lastName || whitespaceRegex.test(state.lastName)) {
			errors.push({ name: 'lastName', message: 'Required.' });
		} else if (state.lastName && !nameRegex.test(state.lastName)) {
			errors.push({
				name: 'lastName',
				message: 'Letters, spaces, and dashes only.',
			});
		}
	}

	if (isProgram(state, entityType)){
		if (!state.programCode || whitespaceRegex.test(state.programCode)) {
			errors.push({ name: 'programCode', message: 'Required.' });
		} else if (state.programCode && !programCodeRegex.test(state.programCode)) {
			errors.push({
				name: 'programCode',
				message: 'Uppercase letters & dashes only.',
			});
		}

		if (!state.programName || whitespaceRegex.test(state.programName)) {
			errors.push({ name: 'programName', message: 'Required.' });
		} else if (state.programName && !programNameRegex.test(state.programName)) {
			console.log('reach here');
			errors.push({
				name: 'programName',
				message: 'Letters, spaces, and dashes only.',
			});
		}
	}

	if (isCollege(state, entityType)){
		if (!state.collegeCode || whitespaceRegex.test(state.collegeCode)) {
			errors.push({ name: 'collegeCode', message: 'Required.' });
		} else if (state.collegeCode && !collegeCodeRegex.test(state.collegeCode)) {
			errors.push({
				name: 'collegeCode',
				message: 'Uppercase letters & dashes only.',
			});
		}

		if (!state.collegeName || whitespaceRegex.test(state.collegeName)) {
			errors.push({ name: 'collegeName', message: 'Required.' });
		} else if (state.collegeName && !collegeNameRegex.test(state.collegeName)) {
			errors.push({
				name: 'collegeName',
				message: 'Letters, spaces, and dashes only.',
			});
		}
	}

  return errors;
};