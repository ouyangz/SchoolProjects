from Tkinter import *
import os
import sys
sys.path.append("..")
import mod.dic

class SmartD_GUI:
    def __init__(self, master=None):
        frame = Frame(master)
        frame.pack()
        
        title = Label(master, text = 'This is THE Smart Dictionary')
        title.pack(side = "top")

        m = PanedWindow(master, orient=HORIZONTAL)
        m.pack(fill = BOTH, side = TOP)

        input_frame = LabelFrame(m, text ="Input Text")
        input_frame.pack(expand = 1, fill = BOTH)

        input_scroll=Scrollbar(input_frame)
        input_scroll.pack(side = RIGHT, fill = Y)

        self.input_text = Text(input_frame, wrap = WORD)
        self.input_text.pack(side = LEFT, fill = Y)
        self.input_text.configure(yscrollcommand = input_scroll.set)
        self.input_text.insert(END, "Please paste your article here, and select the word you want to look up.\n\nThe plane is going to take off shortly. You should put the jacket on. It is dark here, could you turn the light on please?")

        self.input_text.bind('<<Selection>>', self.highlight)

        m.add(input_frame)
        m.paneconfig(input_frame, minsize = 300, padx = 10, pady = 10)

        result_frame = Frame(m, height = 10, width = 30)
        result_frame.pack(expand = 1, fill = BOTH)

        button_explain = Button(result_frame, text = 'Explain', command = self.explain)
        button_explain.pack(side = TOP)

        output_scroll=Scrollbar(result_frame)
        output_scroll.pack(side = RIGHT, fill = Y)

        self.output_text = Text(result_frame, wrap = WORD)
        self.output_text.pack(side = TOP, fill = Y)
        self.output_text.configure(yscrollcommand = output_scroll.set)
        self.output_text.insert(END, "Results")
        self.output_text.configure(state = 'disabled')
        self.output_text.bind("<1>", self.set_focus)

        m.add(result_frame)
        m.paneconfig(result_frame, minsize = 200, padx = 10, pady = 10)

    def set_focus(self, event):
        self.output_text.focus_set()
        
    def highlight(self, event):
        w = self.input_text
        w.tag_delete('Sentence')
        self.sentence_start = w.search(r'[\w][\w][\.\?\'\"\!\?][\s]|[\n]', INSERT, backwards = True, stopindex = '1.0', regexp = True)
        self.sentence_end = w.search(r'[\w][\w][\.\?\'\"\!\?][\s]|[\n]', INSERT, stopindex = END, regexp = True)
        if self.sentence_start == '':
            self.sentence_start = '1.0'
        elif w.get(self.sentence_start) == '\n':
            self.sentence_start += '+1c'
        else:
            self.sentence_start += '+3c'
        if self.sentence_end == '':
            self.sentence_end = END
        elif w.get(self.sentence_end) == '\n':
            self.sentence_end += '+1c'
        else:
            self.sentence_end += '+3c'
        w.tag_add('Sentence', self.sentence_start, self.sentence_end)
        w.tag_config('Sentence', background = 'yellow')
        w.tag_config(SEL, foreground = 'red')

        
    def explain(self):
        input_text = self.input_text
        sentence = input_text.get(self.sentence_start, self.sentence_end)
        word = input_text.get(SEL_FIRST, SEL_LAST)
        result = ''
        # the returned is a list
        possible_chunk, word_expl = mod.dic.Lookup(sentence, word)
        result += possible_chunk
        result += '\n'
        i = 1
        for item in word_expl:
            result += str(i) + '. '
            result += item[0]
            result += '\n'
            if len(item[1]) > 1:
                result += 'Similar words: '
                for lemma_name in item[1]:
                    if lemma_name != possible_chunk:
                        result += lemma_name
                        result += ', '
                result += '\n'
            if len(item[2]) > 0:
                result += 'Examples:\n'
                for example in item[2]:
                    result += '\t\"'
                    result += example
                    result += '\"\n'
            i += 1
        self.output_text.configure(state = 'normal')
        self.output_text.delete('1.0', END)
        self.output_text.insert(END, result )
        self.output_text.configure(state = 'disabled')
        

