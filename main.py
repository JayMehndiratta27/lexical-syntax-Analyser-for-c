import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
import re
from collections import defaultdict

class LineNumberText(scrolledtext.ScrolledText):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create line numbers text widget
        self.line_numbers = tk.Text(
            master,
            width=4,
            padx=3,
            pady=5,
            takefocus=0,
            border=0,
            background='#f0f0f0',
            foreground='#666666',
            state='disabled',
            font=('Consolas', 11)
        )
        
        # Bind events
        self.bind('<Key>', self._on_key)
        self.bind('<MouseWheel>', self._on_mousewheel)
        self.bind('<Configure>', self._on_configure)
        
        # Initial line numbers
        self._update_line_numbers()
    
    def _on_key(self, event=None):
        self._update_line_numbers()
    
    def _on_mousewheel(self, event):
        self.line_numbers.yview_moveto(self.yview()[0])
    
    def _on_configure(self, event=None):
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._update_line_numbers()
    
    def _update_line_numbers(self):
        # Get the number of lines
        line_count = self.get('1.0', tk.END).count('\n') + 1
        
        # Update line numbers
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')
        self.line_numbers.config(state='disabled')
        
        # Sync scrolling
        self.line_numbers.yview_moveto(self.yview()[0])

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='#f0f2f5')  # Light gray background
        self.root.title("C Code Analyzer")
        self.root.geometry("1200x800")  # Slightly larger window
        
        # Configure window to be centered
        self.center_window()
        
        # Set up fonts
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        label_font = font.Font(family="Helvetica", size=11)
        text_font = font.Font(family="Consolas", size=11)
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="C Code Analysis Tool",
            font=title_font,
            background='#f0f2f5'
        )
        title_label.pack(pady=(0, 20))
        
        # Create a frame for the parallel layout
        parallel_frame = ttk.Frame(self.main_frame)
        parallel_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Input section
        left_frame = ttk.Frame(parallel_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_label = ttk.Label(
            left_frame,
            text="Input C Code:",
            font=label_font,
            background='#f0f2f5'
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Create a frame for the input text and line numbers
        input_text_frame = ttk.Frame(left_frame)
        input_text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style for text areas
        text_style = {
            'height': 15,
            'width': 40,
            'wrap': tk.NONE,  # Changed to NONE to prevent wrapping
            'font': text_font,
            'bg': 'white',
            'fg': 'black',
            'insertbackground': 'black',
            'selectbackground': '#3498db',
            'selectforeground': 'white',
            'relief': 'solid',
            'borderwidth': 1
        }
        
        # Create input text with line numbers
        self.input_text = LineNumberText(
            input_text_frame,
            **text_style
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Output section
        right_frame = ttk.Frame(parallel_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        output_label = ttk.Label(
            right_frame,
            text="Analysis Result:",
            font=label_font,
            background='#f0f2f5'
        )
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            **text_style
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_configure('error', foreground='red')
        self.output_text.tag_configure('warning', foreground='orange')
        self.output_text.tag_configure('success', foreground='green')
        self.output_text.tag_configure('info', foreground='blue')
        self.output_text.tag_configure('bold', font=('Consolas', 11, 'bold'))
        
        # SYNTAX HIGHLIGHTING IN INPUT AND OUTPUT
        self.input_text.tag_configure('keyword', foreground='blue')
        self.input_text.tag_configure('string', foreground='green')
        self.input_text.tag_configure('comment', foreground='gray')
        self.input_text.tag_configure('number', foreground='purple')
        self.input_text.tag_configure('operator', foreground='red') # Or a distinct color for operators

        # Bind key release event to trigger highlighting
        self.input_text.bind('<KeyRelease>', self.apply_input_syntax_highlighting)
        # Also trigger on initial load if text is present (optional)
        # self.input_text.after(100, self.apply_input_syntax_highlighting) # Add a small delay
        
        # Buttons frame with styling
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        # Style for buttons
        button_style = {
            'padding': (15, 8),
            'style': 'Accent.TButton'
        }
        
        # Create custom style for buttons
        style = ttk.Style()
        style.configure(
            'Accent.TButton',
            font=('Helvetica', 10, 'bold'),
            background='#3498db',
            foreground='black'
        )
        
        # Analysis buttons
        self.lexical_button = ttk.Button(
            button_frame,
            text="Lexical Analysis",
            command=self.analyze_lexical,
            **button_style
        )
        self.lexical_button.pack(side=tk.LEFT, padx=5)
        
        self.syntax_button = ttk.Button(
            button_frame,
            text="Syntax Analysis",
            command=self.analyze_syntax,
            **button_style
        )
        self.syntax_button.pack(side=tk.LEFT, padx=5)
        
        self.grammar_button = ttk.Button(
            button_frame,
            text="Grammar Analysis",
            command=self.analyze_grammar,
            **button_style
        )
        self.grammar_button.pack(side=tk.LEFT, padx=5)
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def insert_colored_text(self, text, tag=None):
        """Helper method to insert colored text"""
        self.output_text.insert(tk.END, text, tag)
    
    def analyze_lexical(self):
        """Perform lexical analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.insert_colored_text("Please enter some C code.", 'warning')
            return
        
        # Check syntax but continue with analysis
        syntax_errors = self.validate_syntax(input_text)
        self.output_text.delete("1.0", tk.END)
        
        self.insert_colored_text("=== Lexical Analysis ===\n\n", 'bold')
        
        if syntax_errors:
            self.insert_colored_text("Syntax Issues Found (analysis will continue):\n\n", 'warning')
            for error in syntax_errors:
                self.insert_colored_text(f"Line {error['line']}: ", 'error' if error['severity'] == 'error' else 'warning')
                self.insert_colored_text(f"{error['message']}\n", 'error' if error['severity'] == 'error' else 'warning')
                self.insert_colored_text(f"Suggestion: {error['suggestion']}\n", 'info')
            self.insert_colored_text("\n")
        
        try:
            tokens = self.tokenize_c_code(input_text)
            self.insert_colored_text("Tokens Found:\n", 'bold')
            for token_type, token_value in tokens:
                self.insert_colored_text(f"{token_type}: {token_value}\n")
            
            # Add token statistics
            token_counts = defaultdict(int)
            for token_type, _ in tokens:
                token_counts[token_type] += 1
            
            self.insert_colored_text("\nToken Statistics:\n", 'bold')
            for token_type, count in sorted(token_counts.items()):
                self.insert_colored_text(f"{token_type}: {count}\n")
        except Exception as e:
            self.insert_colored_text(f"Error in lexical analysis: {str(e)}", 'error')
    
    def analyze_syntax(self):
        """Perform syntax analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.insert_colored_text("Please enter some C code.", 'warning')
            return
        
        # Check syntax and get detailed errors
        syntax_errors = self.validate_syntax(input_text)
        self.output_text.delete("1.0", tk.END)
        
        self.insert_colored_text("=== Syntax Analysis ===\n\n", 'bold')
        
        if syntax_errors:
            self.insert_colored_text("Issues Found:\n\n", 'bold')
            
            # Group errors by severity
            errors_by_severity = {'error': [], 'warning': []}
            for error in syntax_errors:
                errors_by_severity[error['severity']].append(error)
            
            # Display errors first
            if errors_by_severity['error']:
                self.insert_colored_text("Errors:\n", 'error')
                for error in errors_by_severity['error']:
                    self.insert_colored_text(f"\nLine {error['line']}: ", 'error')
                    self.insert_colored_text(f"{error['message']}\n", 'error')
                    self.insert_colored_text(f"Code: {error['code']}\n")
                    self.insert_colored_text(f"      {' ' * error['position']}^\n")
                    self.insert_colored_text(f"Suggestion: {error['suggestion']}\n", 'info')
            
            # Then display warnings
            if errors_by_severity['warning']:
                self.insert_colored_text("\nWarnings:\n", 'warning')
                for error in errors_by_severity['warning']:
                    self.insert_colored_text(f"\nLine {error['line']}: ", 'warning')
                    self.insert_colored_text(f"{error['message']}\n", 'warning')
                    self.insert_colored_text(f"Code: {error['code']}\n")
                    self.insert_colored_text(f"      {' ' * error['position']}^\n")
                    self.insert_colored_text(f"Suggestion: {error['suggestion']}\n", 'info')
            
            # Add recovery information
            self.insert_colored_text("\nRecovery Information:\n", 'info')
            self.insert_colored_text("- The analyzer will continue processing despite errors\n", 'info')
            self.insert_colored_text("- Fix errors in order of appearance for best results\n", 'info')
            self.insert_colored_text("- Warnings may indicate potential issues that should be reviewed\n", 'info')
            
            # Continue with syntax tree even if there are errors
            try:
                syntax_tree = self.build_c_syntax_tree(input_text)
                self.insert_colored_text("\n\nPartial Syntax Tree (may be incomplete due to errors):\n", 'warning')
                self.insert_colored_text(syntax_tree)
            except Exception as e:
                self.insert_colored_text(f"\n\nCould not generate syntax tree: {str(e)}", 'error')
            return
        
        try:
            syntax_tree = self.build_c_syntax_tree(input_text)
            self.insert_colored_text("No syntax errors found.\n\n", 'success')
            self.insert_colored_text("Syntax Tree:\n", 'bold')
            self.insert_colored_text(syntax_tree)
        except Exception as e:
            self.insert_colored_text(f"Error in syntax analysis: {str(e)}", 'error')
    
    def analyze_grammar(self):
        """Perform grammar analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.insert_colored_text("Please enter some C code.", 'warning')
            return
        
        # Check syntax but continue with analysis
        syntax_errors = self.validate_syntax(input_text)
        self.output_text.delete("1.0", tk.END)
        
        self.insert_colored_text("=== Grammar Analysis ===\n\n", 'bold')
        
        if syntax_errors:
            self.insert_colored_text("Syntax Issues Found (analysis will continue):\n\n", 'warning')
            for error in syntax_errors:
                self.insert_colored_text(f"Line {error['line']}: ", 'error' if error['severity'] == 'error' else 'warning')
                self.insert_colored_text(f"{error['message']}\n", 'error' if error['severity'] == 'error' else 'warning')
                self.insert_colored_text(f"Suggestion: {error['suggestion']}\n", 'info')
            self.insert_colored_text("\n")
        
        try:
            grammar_rules = self.analyze_c_grammar(input_text)
            self.insert_colored_text("Grammar Rules Analysis:\n", 'bold')
            
            # Split grammar rules and color them appropriately
            for rule in grammar_rules.split('\n'):
                if rule.startswith('✓'):
                    self.insert_colored_text(rule + '\n', 'success')
                elif rule.startswith('✗'):
                    self.insert_colored_text(rule + '\n', 'error')
                else:
                    self.insert_colored_text(rule + '\n')
            
            # Add additional grammar statistics
            self.insert_colored_text("\nGrammar Statistics:\n", 'bold')
            self.insert_colored_text(f"Total lines: {len(input_text.split('\n'))}\n")
            self.insert_colored_text(f"Total functions: {len(re.findall(r'\w+\s+\w+\s*\([^)]*\)', input_text))}\n")
            self.insert_colored_text(f"Total control structures: {len(re.findall(r'(if|for|while|do|switch)\s*\(', input_text))}\n")
            self.insert_colored_text(f"Total variable declarations: {len(re.findall(r'(int|char|float|double|void)\s+\w+', input_text))}\n")
        except Exception as e:
            self.insert_colored_text(f"Error in grammar analysis: {str(e)}", 'error')
    
    def validate_syntax(self, code):
        """Validate basic C syntax and return detailed errors with recovery and suggestions"""
        errors = []
        lines = code.split('\n')
        
        # Error recovery state
        recovery_state = {
            'in_function': False,
            'in_control': False,
            'in_block': False,
            'last_valid_token': None,
            'expected_tokens': set(),
            'recovery_mode': False
        }
        
        # Common error patterns and their suggestions
        error_patterns = {
            'missing_semicolon': {
                'pattern': r'^\s*(printf|scanf|return|\w+\s*=|[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\))\s*$',
                'suggestion': "Did you mean to add a semicolon (;) at the end of this statement?"
            },
            'unclosed_brace': {
                'pattern': r'^\s*\{[^}]*$',
                'suggestion': "Did you mean to close this block with a closing brace (})?"
            },
            'unclosed_paren': {
                'pattern': r'^\s*\([^)]*$',
                'suggestion': "Did you mean to close this expression with a closing parenthesis ())?"
            },
            'invalid_declaration': {
                'pattern': r'^\s*(int|char|float|double|void)\s+\w+\s*$',
                'suggestion': "Did you mean to initialize this variable or add a semicolon?"
            }
        }
        
        # Check for main function
        has_main = False
        for i, line in enumerate(lines, 1):
            if re.search(r'^\s*int\s+main\s*\([^)]*\)\s*\{?', line):
                has_main = True
                break
        if not has_main:
            errors.append({
                'line': 1,
                'position': 0,
                'message': "Missing main function",
                'code': "Program must contain a main function",
                'severity': 'error',
                'suggestion': "Add a main function: int main() { ... }"
            })
        
        # Track state
        brace_stack = []
        paren_stack = []
        in_comment = False
        in_string = False
        string_char = None
        in_preprocessor = False
        in_switch_case = False
        
        for i, line in enumerate(lines, 1):
            j = 0
            while j < len(line):
                char = line[j]
                
                # Handle preprocessor directives
                if j == 0 and line.strip().startswith('#'):
                    in_preprocessor = True
                    break
                
                # Skip checking in preprocessor lines
                if in_preprocessor:
                    break
                
                # Handle comments
                if not in_string:
                    if char == '/' and j + 1 < len(line):
                        if line[j + 1] == '/':
                            break  # Skip rest of line for single-line comments
                        elif line[j + 1] == '*':
                            in_comment = True
                            j += 1
                    elif char == '*' and j + 1 < len(line) and line[j + 1] == '/':
                        if not in_comment:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected comment end '*/'",
                                'code': line,
                                'severity': 'warning',
                                'suggestion': "Remove unexpected comment end or add a comment start '/*'"
                            })
                        in_comment = False
                        j += 1
                
                # Handle strings
                if not in_comment:
                    if char in ['"', "'"]:
                        if not in_string:
                            in_string = True
                            string_char = char
                        elif char == string_char and line[j-1] != '\\':  # Handle escaped quotes
                            in_string = False
                
                # Only check braces and parentheses when not in comments or strings
                if not in_comment and not in_string:
                    if char == '{':
                        brace_stack.append((i, j))
                        recovery_state['in_block'] = True
                    elif char == '}':
                        if not brace_stack:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected closing brace '}'",
                                'code': line,
                                'severity': 'error',
                                'suggestion': "Remove unexpected closing brace or add an opening brace '{'"
                            })
                        else:
                            brace_stack.pop()
                            recovery_state['in_block'] = False
                    elif char == '(':
                        paren_stack.append((i, j))
                    elif char == ')':
                        if not paren_stack:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected closing parenthesis ')'",
                                'code': line,
                                'severity': 'error',
                                'suggestion': "Remove unexpected closing parenthesis or add an opening parenthesis '('"
                            })
                        else:
                            paren_stack.pop()
                
                j += 1
            
            # Reset preprocessor state for next line
            in_preprocessor = False
            
            # Check for common error patterns
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('/*') and not line.startswith('#'):
                for error_type, pattern_info in error_patterns.items():
                    if re.match(pattern_info['pattern'], line):
                        errors.append({
                            'line': i,
                            'position': len(line),
                            'message': f"Potential {error_type.replace('_', ' ')}",
                            'code': line,
                            'severity': 'warning',
                            'suggestion': pattern_info['suggestion']
                        })
        
        # Report unclosed braces and parentheses with recovery suggestions
        for line, pos in brace_stack:
            errors.append({
                'line': line,
                'position': pos,
                'message': "Unclosed brace '{'",
                'code': lines[line-1],
                'severity': 'error',
                'suggestion': "Add a closing brace '}' to match the opening brace"
            })
        
        for line, pos in paren_stack:
            errors.append({
                'line': line,
                'position': pos,
                'message': "Unclosed parenthesis '('",
                'code': lines[line-1],
                'severity': 'error',
                'suggestion': "Add a closing parenthesis ')' to match the opening parenthesis"
            })
        
        # Check for unclosed comments
        if in_comment:
            errors.append({
                'line': len(lines),
                'position': len(lines[-1]),
                'message': "Unclosed comment '/*'",
                'code': lines[-1],
                'severity': 'error',
                'suggestion': "Add a comment end '*/' to close the comment"
            })
        
        # Check for unclosed strings
        if in_string:
            errors.append({
                'line': len(lines),
                'position': len(lines[-1]),
                'message': f"Unclosed string (started with {string_char})",
                'code': lines[-1],
                'severity': 'error',
                'suggestion': f"Add a closing quote {string_char} to end the string"
            })
        
        # Sort errors by line number and severity
        errors.sort(key=lambda x: (x['line'], 0 if x['severity'] == 'error' else 1))
        
        return errors
    
    def tokenize_c_code(self, code):
        """Tokenize C code into meaningful components"""
        tokens = []
        lines = code.split('\n')
        
        # C keywords
        c_keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }
        
        # C operators
        c_operators = {
            '+', '-', '*', '/', '%', '++', '--', '=', '+=', '-=', '*=', '/=', '%=',
            '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~',
            '<<', '>>', '->', '?', ':'
        }

        c_seperator = {
            '(', ')', '{', '}', '[', ']',
            ',', '.', ';'
        }
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Handle preprocessor directives
            if line.strip().startswith('#'):
                tokens.append(('PREPROCESSOR', line.strip()))
                continue
            
            # Handle comments
            if '//' in line:
                comment_start = line.find('//')
                code_part = line[:comment_start]
                comment_part = line[comment_start:]
                if code_part.strip():
                    self._tokenize_line(code_part, tokens, c_keywords, c_operators, c_seperator)
                tokens.append(('COMMENT', comment_part))
                continue
            
            # Handle multi-line comments
            if '/*' in line:
                tokens.append(('COMMENT_START', '/*'))
                continue
            if '*/' in line:
                tokens.append(('COMMENT_END', '*/'))
                continue
            
            # Tokenize the line
            self._tokenize_line(line, tokens, c_keywords, c_operators, c_seperator)
        
        return tokens
    
    def _tokenize_line(self, line, tokens, c_keywords, c_operators, c_seperator):
        """Helper function to tokenize a single line of C code"""
        # Split the line into words
        words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|"[^"]*"|\'[^\']*\'|[-+*/%=<>!&|^~?:;,.()\[\]{}]|->|\.', line)
        
        for word in words:
            if word in c_keywords:
                tokens.append(('KEYWORD', word))
            elif word in c_operators:
                tokens.append(('OPERATOR', word))
            elif word in c_seperator:
                tokens.append(('SEPARATOR', word))
            elif word.startswith('"') or word.startswith("'"):
                tokens.append(('STRING', word))
            elif word.isdigit():
                tokens.append(('NUMBER', word))
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', word):
                tokens.append(('IDENTIFIER', word))
            else:
                tokens.append(('UNKNOWN', word))
    
    def build_c_syntax_tree(self, code):
        """Build a syntax tree for C code"""
        tree = []
        current_level = 0
        in_function = False
        in_block = False
        
        for line in code.split('\n'):
            if not line.strip():
                continue
            
            # Skip comments
            if line.strip().startswith('//') or '/*' in line or '*/' in line:
                continue
            
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            level = indent // 4  # Assuming 4 spaces per indentation level
            
            # Handle function definitions
            if re.match(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$', line):
                in_function = True
                tree.append('  ' * level + '└── Function: ' + line.strip())
                continue
            
            # Handle control structures
            if re.match(r'^\s*(if|for|while|do|switch)\s*\(', line):
                tree.append('  ' * level + '└── Control: ' + line.strip())
                in_block = True
                continue
            
            # Handle blocks
            if '{' in line:
                tree.append('  ' * level + '└── Block Start')
                in_block = True
                continue
            if '}' in line:
                tree.append('  ' * level + '└── Block End')
                in_block = False
                continue
            
            # Handle statements
            if ';' in line:
                tree.append('  ' * level + '└── Statement: ' + line.strip())
                continue
            
            # Handle other lines
            tree.append('  ' * level + '└── ' + line.strip())
        
        return '\n'.join(tree)
    
    def analyze_c_grammar(self, code):
        """Analyze C code grammar and structure"""
        rules = []
        
        # Check for main function
        if re.search(r'int\s+main\s*\([^)]*\)', code):
            rules.append("✓ Main function found")
        else:
            rules.append("✗ Main function not found")
        
        # Check for proper header inclusion
        if re.search(r'#include\s+<[^>]+>', code):
            rules.append("✓ Header files included")
        
        # Check for function definitions
        functions = re.findall(r'\w+\s+\w+\s*\([^)]*\)', code)
        if functions:
            rules.append(f"✓ Found {len(functions)} function(s):")
            for func in functions:
                rules.append(f"  - {func}")
        
        # Check for control structures
        if re.search(r'if\s*\([^)]*\)', code):
            rules.append("✓ If statements present")
        if re.search(r'for\s*\([^)]*\)', code):
            rules.append("✓ For loops present")
        if re.search(r'while\s*\([^)]*\)', code):
            rules.append("✓ While loops present")
        
        # Check for proper block structure
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces == close_braces:
            rules.append("✓ Balanced braces")
        else:
            rules.append(f"✗ Unbalanced braces: {open_braces} opening, {close_braces} closing")
        
        # Check for variable declarations
        if re.search(r'\w+\s+\w+\s*=', code):
            rules.append("✓ Variable declarations found")
        
        # Check for proper semicolon usage
        statements = code.count(';')
        if statements > 0:
            rules.append(f"✓ Found {statements} statements")
        
        # Check for proper indentation
        lines = code.split('\n')
        indent_levels = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        if all(level % 4 == 0 for level in indent_levels):
            rules.append("✓ Proper indentation (4 spaces)")
        else:
            rules.append("✗ Inconsistent indentation")
        
        return "\n".join(rules)

    def apply_input_syntax_highlighting(self, event=None):
        """Apply syntax highlighting to the input text widget."""
        input_text_widget = self.input_text # self.input_text is now LineNumberText, which is the main text widget

        # Remove all existing tags
        for tag in input_text_widget.tag_names():
             if tag not in ('linenumbers', 'currentline'): # Keep line number and current line tags
                 input_text_widget.tag_remove(tag, '1.0', tk.END)

        code = input_text_widget.get('1.0', tk.END)
        lines = code.split('\n')

        # C keywords, operators, and separators (reuse from tokenize_c_code if possible, or define here)
        c_keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }
        c_operators_seperators = {
            '+', '-', '*', '/', '%', '++', '--', '=', '+=', '-=', '*=', '/=', '%=',
            '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~',
            '<<', '>>', '->', '?', ':', '(', ')', '{', '}', '[', ']', ',', '.', ';'
        }


        # Apply highlighting line by line
        for i, line in enumerate(lines):
            line_number = i + 1
            start_index = f'{line_number}.0'
            end_index = f'{line_number}.{len(line)}'

            # Highlight comments (single line)
            comment_match = re.search(r'//.*', line)
            if comment_match:
                comment_start = f'{line_number}.{comment_match.start()}'
                comment_end = f'{line_number}.{comment_match.end()}'
                input_text_widget.tag_add('comment', comment_start, comment_end)

            # Highlight strings
            for match in re.finditer(r'"([^"\\]*(\\.)?)*"|\'([^\'\\]*(\\.)?)*\'', line):
                str_start = f'{line_number}.{match.start()}'
                str_end = f'{line_number}.{match.end()}'
                input_text_widget.tag_add('string', str_start, str_end)

            # Highlight numbers
            for match in re.finditer(r'\b\d+\b', line):
                 num_start = f'{line_number}.{match.start()}'
                 num_end = f'{line_number}.{match.end()}'
                 input_text_widget.tag_add('number', num_start, num_end)

            # Highlight keywords and operators/separators (careful not to highlight within strings/comments)
            # This is a simplified approach; a full lexer would be more robust
            temp_line = line # Use a temp line to replace parts already tagged
            replacements = []

            # Mark strings and comments as placeholders
            for match in re.finditer(r'"([^"\\]*(\\.)?)*"|\'([^\'\\]*(\\.)?)*\'|//.*', temp_line):
                 replacements.append((match.start(), match.end(), ' ' * (match.end() - match.start())))

            # Apply replacements in reverse order to keep indices valid
            replacements.sort(key=lambda x: x[0], reverse=True)
            for start, end, placeholder in replacements:
                temp_line = temp_line[:start] + placeholder + temp_line[end:]

            # Now find keywords and operators/separators in the modified line
            for match in re.finditer(r'\b\w+\b|[-+*/%=<>!&|^~?:;,.()\[\]{}]|->|\.', temp_line):
                word = match.group(0)
                word_start_col = match.start()
                word_end_col = match.end()
                word_start_index = f'{line_number}.{word_start_col}'
                word_end_index = f'{line_number}.{word_end_col}'

                if word in c_keywords:
                    input_text_widget.tag_add('keyword', word_start_index, word_end_index)
                elif word in c_operators_seperators:
                     input_text_widget.tag_add('operator', word_start_index, word_end_index)


# Run the application
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()
