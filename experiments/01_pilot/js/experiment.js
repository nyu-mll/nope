// set up experiment logic for each slide
function make_slides(f) {
  var slides = {};

  // set up initial slide
  slides.i0 = slide({
    name: "i0",
    start: function() {
      exp.startT = Date.now();
    }
  });


  // set up slide with instructions for main experiment
  slides.startExp = slide({
    name: "startExp",
    start: function() {
    },
    button: function() {
      exp.go(); //use exp.go() if and only if there is no "present" data.
    },
  });

  slides.trial = slide({
    name: "trial",
     present: exp.stimuli,
     present_handle : function(stim) {


      // store stimulus data
      this.stim = stim;

      // extract original and sentence with "but not all"
      // var original_sentence = stim.EntireSentence;
      // var target_sentence = stim.ButNotAllSentence;
      //
      // //handle display of context
      //  if (exp.condition == "context") {
      //    // extract context data
      //    var contexthtml = stim.Context;
      //    // reformat the speaker information for context
      //    contexthtml = contexthtml.replace(/Speaker A:/g, "<b>Speaker #1:</b>");
      //    contexthtml = contexthtml.replace(/Speaker B:/g, "<b>Speaker #2:</b>");
      //    $(".case").html(contexthtml);
      //  } else {
      //    var contexthtml = "";
      //    $(".case").html(contexthtml);
      //  }
      //
      // // replace the placeholder in the HTML document with the relevant sentences for this trial
      // $("#trial-originalSen").html(original_sentence);
      // $("#trial-targetSen").html(target_sentence);

      function build_premise() {
        var anon_speakers = ["Speaker A", "Speaker B", "Speaker C"];
        var all_speakers = {}

        all_speakers[stim.premise_speaker] =  anon_speakers.shift();

        if (stim.context1.length > 0 && !(stim.context1_speaker in all_speakers)) {
          all_speakers[stim.context1_speaker] = anon_speakers.shift();
        }
        if (stim.context2.length > 0 && !(stim.context2_speaker in all_speakers)) {
          all_speakers[stim.context2_speaker] = anon_speakers.shift();
        }

        var premise = "";
        if (stim.context1.length > 0) {
          premise += "<strong>" + all_speakers[stim.context1_speaker] + "</strong>: " + stim.context1;
          if (stim.context1_speaker != stim.context2_speaker) {
              premise += "<br><strong>" + all_speakers[stim.context2_speaker] + "</strong>:"
          }
        } else if (stim.context2.length > 0) {
          premise += "<strong>" + all_speakers[stim.context2_speaker] + "</strong>:"
        }
        if (stim.context2.length > 0) {
          premise += " " + stim.context2;
          if (stim.context2_speaker != stim.premise_speaker) {
              premise += "<br><strong>" + all_speakers[stim.premise_speaker] + "</strong>:"
          }
        } else {
          premise += "<strong>" + all_speakers[stim.premise_speaker] + "</strong>:"
        }
        premise += " " + stim.premise;

        return premise;
      }




      $("#trial-premise").html(build_premise());

      $("#trial-hypothesis").text(stim.hypothesis);
      utils.make_slider("#trial-slider", function() {
        var changed_val = !$("#trial-slider .ui-slider-handle").is(":hidden");
        if (!changed_val) {
          $("#slider-val").text("--");
          return;
        }
        var val = $(this).slider("option", "value");
        var transformed_val = ((100/(1 + Math.pow((-1 + 1/val), 1.5)))).toFixed(2);
        $("#slider-val").text(transformed_val);
      });
      $(".err").hide();
      $("#slider-val").text("--");
    },

    // handle click on "Continue" button
    button: function() {
      var changed_val = !$("#trial-slider .ui-slider-handle").is(":hidden");

      if (changed_val) {
        this.log_responses();
         _stream.apply(this);
      } else {
        $('.err').show();
      }
    },

    // save response
    log_responses: function() {
      exp.data_trials.push({
        "id": this.stim.sent_id,
        "context1": this.stim.context1,
        "context2": this.stim.context2,
        "premise": this.stim.premise,
        "hypothesis": this.stim.hypothesis,
        "context1_speaker": this.stim.context1_speaker,
        "context2_speaker": this.stim.context2_speaker,
        "premise_speaker": this.stim.premise_speaker,
        "trial": exp.phase, //exp.phase is a built-in trial number tracker
        "response": $("#slider-val").text(),
      });
    },
  });

  // slide to collect subject information
  slides.subj_info = slide({
    name: "subj_info",
    submit: function(e) {
      exp.subj_data = {
        language: $("#language").val(),
        enjoyment: $("#enjoyment").val(),
        asses: $('input[name="assess"]:checked').val(),
        age: $("#age").val(),
        gender: $("#gender").val(),
        education: $("#education").val(),
        fairprice: $("#fairprice").val(),
        comments: $("#comments").val()
      };
      exp.go(); //use exp.go() if and only if there is no "present" data.
    }
  });

  //
  slides.thanks = slide({
    name: "thanks",
    start: function() {
      exp.data = {
        "trials": exp.data_trials,
        "catch_trials": exp.catch_trials,
        "system": exp.system,
        "condition": exp.condition,
        "subject_information": exp.subj_data,
        "time_in_minutes": (Date.now() - exp.startT) / 60000
      };
      setTimeout(function () {
        turk.submit(exp.data);
      }, 1000);
    }
  });

  return slides;
}

/// initialize experiment
function init() {

  exp.trials = [];
  exp.catch_trials = [];
  var stimuli = all_stims;

  exp.stimuli = stimuli; //call _.shuffle(stimuli) to randomize the order;
  exp.n_trials = exp.stimuli.length;

   exp.condition = _.sample(["context", "no-context"]); //can randomize between subjects conditions here

  exp.system = {
    Browser: BrowserDetect.browser,
    OS: BrowserDetect.OS,
    screenH: screen.height,
    screenUH: exp.height,
    screenW: screen.width,
    screenUW: exp.width
  };

  //blocks of the experiment:
  exp.structure = [
    "i0",
    "startExp",
    "trial",
    "subj_info",
    "thanks"
  ];

  exp.data_trials = [];

  //make corresponding slides:
  exp.slides = make_slides(exp);

  exp.nQs = utils.get_exp_length();
  //this does not work if there are stacks of stims (but does work for an experiment with this structure)
  //relies on structure and slides being defined

  $('.slide').hide(); //hide everything

  $("#start_button").click(function() {
    exp.go();
  });

  exp.go(); //show first slide
}
