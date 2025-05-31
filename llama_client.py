import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LlamaProcessor:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("LLAMA_API_KEY"), 
            base_url="https://api.llama.com/compat/v1/"
        )
    
    def load_person_data(self, filename="person_data.json"):
        """
        Load person data from JSON file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"❌ Error: {filename} not found. Please run crustdata.py first.")
            return None
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in {filename}")
            return None
    
    def analyze_job_fit(self, job_description, filename="person_data.json"):
        """
        Analyze if the person is a good fit for a specific job
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        prompt = self._create_job_fit_prompt(person, job_description)
        
        try:
            completion = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error processing with Llama API: {str(e)}"
    
    def general_analysis(self, filename="person_data.json"):
        """
        General professional analysis of the person
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        prompt = self._create_general_prompt(person)
        
        try:
            completion = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error processing with Llama API: {str(e)}"
    
    def simple_chat(self, filename="person_data.json"):
        """
        Simple chat interface to ask questions about the person data
        """
        person_data = self.load_person_data(filename)
        if not person_data:
            return "Unable to load person data."
        
        # Handle list format from CrustData API
        if isinstance(person_data, list) and len(person_data) > 0:
            person = person_data[0]  # Get the first person
        else:
            person = person_data
        
        print("\n🤖 Simple Chat Mode - Ask me anything about the person data!")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_question = input("You: ").strip()
            
            if user_question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_question:
                continue
            
            # Create a simple prompt with the person data and user question
            prompt = f"""
            Based on the following person data, please answer the user's question:

            Person Data:
            {json.dumps(person, indent=2)}

            User Question: {user_question}

            Please provide a helpful and accurate answer based on the data above.
            """
            
            try:
                completion = self.client.chat.completions.create(
                    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )
                response = completion.choices[0].message.content
                print(f"\n🤖 Assistant: {response}\n")
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")

    def _create_job_fit_prompt(self, person_data, job_description):
        """
        Create a prompt to analyze job fit
        """
        name = person_data.get('name', 'Unknown')
        current_title = person_data.get('current_position_title', 'Unknown')
        current_company = person_data.get('current_company_name', 'Unknown')
        
        # Extract work experience
        work_experience = []
        if 'work_experience' in person_data:
            for exp in person_data['work_experience'][:5]:  # Last 5 positions
                work_experience.append(f"• {exp.get('employee_title', 'Unknown')} at {exp.get('employer_name', 'Unknown')}")
        
        # Extract education
        education = []
        if 'education_background' in person_data:
            for edu in person_data['education_background']:
                degree = edu.get('degree_name', 'Unknown')
                school = edu.get('institute_name', 'Unknown')
                field = edu.get('field_of_study', '')
                education.append(f"• {degree} in {field} from {school}")
        
        prompt = f"""
        JOB FIT ANALYSIS REQUEST
        
        CANDIDATE PROFILE:
        Name: {name}
        Current Position: {current_title} at {current_company}
        
        Recent Work Experience:
        {chr(10).join(work_experience) if work_experience else '• No work experience data available'}
        
        Education:
        {chr(10).join(education) if education else '• No education data available'}
        
        JOB DESCRIPTION:
        {job_description}
        
        ANALYSIS REQUEST:
        Please analyze if this candidate is a good fit for the job described above. Provide:
        
        1. **FIT SCORE** (1-10): Rate how well this candidate matches the job requirements
        
        2. **STRENGTHS**: What makes this candidate a good fit? List specific experiences, skills, or qualifications that align with the job.
        
        3. **GAPS**: What are the potential gaps or concerns? What might the candidate lack for this role?
        
        4. **RECOMMENDATION**: Should we proceed with this candidate? Why or why not?
        
        5. **NEXT STEPS**: If moving forward, what questions should we ask in an interview to validate fit?
        
        Format your response clearly with the numbered sections above.
        """
        
        return prompt
    
    def _create_general_prompt(self, person_data):
        """
        Create a general analysis prompt
        """
        name = person_data.get('name', 'Unknown')
        current_title = person_data.get('current_position_title', 'Unknown')
        current_company = person_data.get('current_company_name', 'Unknown')
        
        prompt = f"""
        PROFESSIONAL PROFILE ANALYSIS
        
        Candidate: {name}
        Current Role: {current_title} at {current_company}
        
        Full Profile Data:
        {json.dumps(person_data, indent=2)}
        
        Please provide a comprehensive professional analysis including:
        
        1. **Professional Summary**: Brief overview of their career
        2. **Key Strengths**: Core skills and expertise areas
        3. **Career Progression**: How their career has evolved
        4. **Industry Focus**: What industries/domains they specialize in
        5. **Unique Value**: What makes them stand out
        6. **Potential Opportunities**: Types of roles they'd be good for
        
        Format your response in a clear, structured way.
        """
        
        return prompt

def main():
    """
    Main function to run job fit analysis
    """
    processor = LlamaProcessor()
    
    print("=== LLAMA AI PROCESSOR ===\n")
    
    # Check if person data exists
    if not os.path.exists("person_data.json"):
        print("❌ No person data found. Please run 'python crustdata.py' first to fetch data.")
        return
    
    print("Choose analysis type:")
    print("1. Job Fit Analysis (compare candidate to job description)")
    print("2. General Professional Analysis")
    print("3. Simple Chat (ask questions about the person data)")
    
    choice = input("\nEnter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\n📝 Please enter the job description:")
        job_description = input()
        
        if job_description.strip():
            print("\n🤖 Analyzing job fit...")
            result = processor.analyze_job_fit(job_description)
            print("\n" + "="*50)
            print("JOB FIT ANALYSIS RESULTS")
            print("="*50)
            print(result)
        else:
            print("❌ Job description cannot be empty.")
    
    elif choice == "2":
        print("\n🤖 Performing general analysis...")
        result = processor.general_analysis()
        print("\n" + "="*50)
        print("PROFESSIONAL ANALYSIS RESULTS")
        print("="*50)
        print(result)
    
    elif choice == "3":
        processor.simple_chat()
    
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
